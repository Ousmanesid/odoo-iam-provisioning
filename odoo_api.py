#!/usr/bin/env python3
"""
Système de provisionnement IAM pour Odoo
Partie 3: API de provisionnement FastAPI

Auteur: Système IAM Odoo
Date: 2025-05-28
"""

import xmlrpc.client
import random
import string
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

# Configuration Odoo
ODOO_URL = "http://localhost:8069"
ODOO_DB = "odoo_db"
ODOO_USERNAME = "admin"
ODOO_PASSWORD = "admin"  # Mot de passe par défaut Odoo

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation FastAPI
app = FastAPI(
    title="API de Provisionnement Odoo",
    description="API pour créer, modifier et supprimer des comptes utilisateurs dans Odoo",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes depuis React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Port de développement React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connexion Odoo
try:
    common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    if not uid:
        raise Exception("Erreur d'authentification Odoo")
    logger.info(f"Connexion Odoo réussie - UID: {uid}")
except Exception as e:
    logger.error(f"Erreur de connexion Odoo: {e}")
    uid = None

# Modèles Pydantic pour la validation des données

class AccountAdditionalIds(BaseModel):
    id: str = ""  # CN=John Doe,OU=Users,DC=example,DC=com
    guid: str = ""  # UUID
    up_id: str = ""  # User Principal ID
    display_name: str = ""

class UserAccount(BaseModel):
    login_name: str
    other_ids: AccountAdditionalIds

class GroupAdditionalIds(BaseModel):
    guid: str = ""
    display_name: str = ""
    extra_info1: str = ""
    extra_info2: str = ""
    extra_info3: str = ""

class GroupInfo(BaseModel):
    external_name: str
    other_ids: GroupAdditionalIds

class CreateUserRequest(BaseModel):
    user_account: UserAccount
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    groups: Optional[List[int]] = []

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    login: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    groups: Optional[List[int]] = None

class AssignRolesRequest(BaseModel):
    groups: List[int]

# Fonctions utilitaires

def generate_password(length: int = 12) -> str:
    """Génère un mot de passe aléatoire sécurisé"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(chars) for _ in range(length))
    
    # Assurer qu'il y a au moins une majuscule, une minuscule, un chiffre et un caractère spécial
    if not any(c.isupper() for c in password):
        password = password[:-1] + random.choice(string.ascii_uppercase)
    if not any(c.islower() for c in password):
        password = password[:-1] + random.choice(string.ascii_lowercase)
    if not any(c.isdigit() for c in password):
        password = password[:-1] + random.choice(string.digits)
    if not any(c in "!@#$%^&*" for c in password):
        password = password[:-1] + random.choice("!@#$%^&*")
        
    return password

def validate_odoo_connection():
    """Valide que la connexion Odoo est active"""
    if not uid:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service Odoo non disponible"
        )

# Endpoints de l'API

@app.get("/")
def read_root():
    """Endpoint racine pour vérifier le statut de l'API"""
    return {
        "message": "API de Provisionnement Odoo",
        "version": "1.0.0",
        "odoo_connected": uid is not None
    }

@app.get("/health")
def health_check():
    """Vérification de l'état de santé de l'API"""
    return {
        "status": "healthy" if uid else "unhealthy",
        "odoo_connection": uid is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(request: CreateUserRequest):
    """
    III.1: Endpoint pour créer un utilisateur
    Prend en compte la structure JSON cupws__AccountId__AccountAdditionalIds
    """
    validate_odoo_connection()
    
    try:
        # Extraction des données
        login_name = request.user_account.login_name
        display_name = request.user_account.other_ids.display_name or request.name or login_name
        email = request.email or login_name
        password = request.password or generate_password()
        groups = request.groups or []
        
        # Création de l'utilisateur dans Odoo
        user_data = {
            'name': display_name,
            'login': login_name,
            'email': email,
            'password': password,
            'active': True,
            'groups_id': [(6, 0, groups)] if groups else []
        }
        
        # Ajout des métadonnées si disponibles
        if request.user_account.other_ids.up_id:
            user_data['employee_id'] = request.user_account.other_ids.up_id
        
        user_id = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD, 
            'res.users', 'create', 
            [user_data]
        )
        
        logger.info(f"Utilisateur créé: {display_name} (ID: {user_id})")
        
        return {
            "user_id": user_id,
            "message": "Utilisateur créé avec succès",
            "login": login_name,
            "password": password if not request.password else "***",
            "groups": groups
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la création de l'utilisateur: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de l'utilisateur: {str(e)}"
        )

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Récupérer les informations d'un utilisateur"""
    validate_odoo_connection()
    
    try:
        user = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.users', 'read',
            [user_id], {'fields': ['name', 'login', 'email', 'active', 'groups_id']}
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        return user[0]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'utilisateur {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération de l'utilisateur: {str(e)}"
        )

@app.put("/users/{user_id}")
def update_user(user_id: int, request: UpdateUserRequest):
    """
    III.2: Endpoint pour modifier un utilisateur
    """
    validate_odoo_connection()
    
    try:
        # Vérifier que l'utilisateur existe
        existing_user = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.users', 'search',
            [[('id', '=', user_id)]]
        )
        
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        # Construire les valeurs à mettre à jour
        values = {}
        if request.name:
            values['name'] = request.name
        if request.login:
            values['login'] = request.login
        if request.email:
            values['email'] = request.email
        if request.password:
            values['password'] = request.password
        if request.groups is not None:
            values['groups_id'] = [(6, 0, request.groups)]
        
        if not values:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aucune valeur à mettre à jour"
            )
        
        # Mise à jour
        result = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.users', 'write',
            [[user_id], values]
        )
        
        if result:
            logger.info(f"Utilisateur {user_id} mis à jour")
            return {"message": "Utilisateur mis à jour avec succès", "user_id": user_id}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Échec de la mise à jour"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour de l'utilisateur {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour: {str(e)}"
        )

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """
    III.3: Endpoint pour supprimer un utilisateur
    """
    validate_odoo_connection()
    
    try:
        # Vérifier que l'utilisateur existe
        existing_user = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.users', 'read',
            [user_id], {'fields': ['name', 'login']}
        )
        
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        # Suppression
        result = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.users', 'unlink',
            [[user_id]]
        )
        
        if result:
            logger.info(f"Utilisateur {user_id} supprimé: {existing_user[0]['name']}")
            return {"message": "Utilisateur supprimé avec succès", "user_id": user_id}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Échec de la suppression"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de l'utilisateur {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression: {str(e)}"
        )

@app.post("/users/full", status_code=status.HTTP_201_CREATED)
def create_user_with_roles(request: CreateUserRequest):
    """
    III.4: Endpoint pour créer un utilisateur avec groupes en une seule opération
    """
    # Cette fonction est identique à create_user mais plus explicite
    return create_user(request)

@app.get("/users/{user_id}/roles")
def get_user_roles(user_id: int):
    """
    III.5: Endpoint pour lister les rôles/permissions d'un utilisateur
    """
    validate_odoo_connection()
    
    try:
        # Récupérer les groupes de l'utilisateur
        user = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.users', 'read',
            [user_id], {'fields': ['groups_id']}
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        group_ids = user[0]['groups_id']
        
        if not group_ids:
            return {"user_id": user_id, "groups": [], "message": "Aucun groupe assigné"}
        
        # Récupérer les détails des groupes
        groups = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.groups', 'read',
            [group_ids], {'fields': ['name', 'category_id']}
        )
        
        return {
            "user_id": user_id,
            "groups": groups,
            "total_groups": len(groups)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des rôles de l'utilisateur {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des rôles: {str(e)}"
        )

@app.post("/users/{user_id}/roles")
def assign_roles(user_id: int, request: AssignRolesRequest):
    """
    III.6: Endpoint pour attribuer des rôles à un utilisateur
    """
    validate_odoo_connection()
    
    try:
        # Vérifier que l'utilisateur existe
        user = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.users', 'read',
            [[user_id]], {'fields': ['groups_id']}
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        existing_groups = user[0]['groups_id']
        new_groups = list(set(existing_groups + request.groups))
        
        # Mise à jour des groupes
        result = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.users', 'write',
            [[user_id], {'groups_id': [(6, 0, new_groups)]}]
        )
        
        if result:
            logger.info(f"Rôles attribués à l'utilisateur {user_id}: {request.groups}")
            return {
                "message": "Rôles attribués avec succès",
                "user_id": user_id,
                "groups": new_groups,
                "added_groups": request.groups
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Échec de l'attribution des rôles"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de l'attribution des rôles à l'utilisateur {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'attribution des rôles: {str(e)}"
        )

@app.delete("/users/{user_id}/roles")
def remove_roles(user_id: int, request: AssignRolesRequest):
    """
    III.7: Endpoint pour retirer des rôles d'un utilisateur
    """
    validate_odoo_connection()
    
    try:
        # Vérifier que l'utilisateur existe
        user = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.users', 'read',
            [[user_id]], {'fields': ['groups_id']}
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        existing_groups = user[0]['groups_id']
        updated_groups = [group for group in existing_groups if group not in request.groups]
        
        # Mise à jour des groupes
        result = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.users', 'write',
            [[user_id], {'groups_id': [(6, 0, updated_groups)]}]
        )
        
        if result:
            logger.info(f"Rôles retirés de l'utilisateur {user_id}: {request.groups}")
            return {
                "message": "Rôles retirés avec succès",
                "user_id": user_id,
                "groups": updated_groups,
                "removed_groups": request.groups
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Échec du retrait des rôles"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors du retrait des rôles de l'utilisateur {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du retrait des rôles: {str(e)}"
        )

@app.get("/groups/")
def list_groups():
    """Endpoint pour lister tous les groupes disponibles"""
    validate_odoo_connection()
    
    try:
        groups = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.groups', 'search_read',
            [[]], {'fields': ['name', 'category_id', 'comment']}
        )
        
        return {
            "groups": groups,
            "total": len(groups)
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des groupes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des groupes: {str(e)}"
        )

@app.get("/groups/search/{group_name}")
def search_group_by_name(group_name: str):
    """Rechercher un groupe par nom"""
    validate_odoo_connection()
    
    try:
        groups = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.groups', 'search_read',
            [[('name', 'ilike', group_name)]], 
            {'fields': ['name', 'category_id', 'comment']}
        )
        
        return {
            "groups": groups,
            "total": len(groups),
            "search_term": group_name
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la recherche du groupe '{group_name}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la recherche du groupe: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 