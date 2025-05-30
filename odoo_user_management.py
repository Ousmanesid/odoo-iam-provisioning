#!/usr/bin/env python3
"""
Système de provisionnement IAM pour Odoo
Partie 2: Modification et suppression des comptes utilisateurs existants

Auteur: Système IAM Odoo
Date: 2025-05-28
"""

import xmlrpc.client
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List

# Configuration Odoo
ODOO_URL = "http://localhost:8069"
ODOO_DB = "odoo_db"
ODOO_USER = "admin"
ODOO_PASSWORD = "admin"

# Configuration du logging
LOG_FILE = "odoo_user_management.log"

class OdooUserManagement:
    """Classe pour la gestion des utilisateurs Odoo existants"""
    
    def __init__(self):
        self.setup_logging()
        self.common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        self.models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
        self.uid = None
        
    def setup_logging(self):
        """Configuration du système de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_FILE, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def log_operation(self, function_name: str, operation_data: Dict, result: Any, success: bool):
        """Enregistre une opération dans le fichier de log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "SUCCÈS" if success else "ÉCHEC"
        
        log_entry = f"{timestamp} | {function_name} | {status} | Données: {operation_data} | Résultat: {result}"
        
        with open(LOG_FILE, 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry + "\n")
            
        if success:
            self.logger.info(f"{function_name} - {status}")
        else:
            self.logger.error(f"{function_name} - {status}: {result}")
    
    def authenticate(self) -> Optional[int]:
        """Authentifie l'utilisateur et retourne l'UID de session"""
        try:
            self.uid = self.common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
            if self.uid:
                self.log_operation("authenticate", 
                                 {"db": ODOO_DB, "user": ODOO_USER}, 
                                 f"UID: {self.uid}", True)
                return self.uid
            else:
                self.log_operation("authenticate", 
                                 {"db": ODOO_DB, "user": ODOO_USER}, 
                                 "Authentification échouée", False)
                return None
        except Exception as e:
            self.log_operation("authenticate", 
                             {"db": ODOO_DB, "user": ODOO_USER}, 
                             f"Erreur: {str(e)}", False)
            return None
    
    def user_exists(self, username: str) -> Optional[int]:
        """
        II.1: Recherche si un compte utilisateur existe dans la base Odoo
        Retourne l'ID de l'utilisateur si trouvé, None sinon
        """
        try:
            if not self.uid:
                self.uid = self.authenticate()
                if not self.uid:
                    return None
            
            # Recherche par login (email ou nom d'utilisateur)
            user_ids = self.models.execute_kw(
                ODOO_DB, self.uid, ODOO_PASSWORD, 
                'res.users', 'search', 
                [[('login', '=', username)]]
            )
            
            if user_ids:
                user_id = user_ids[0]
                self.log_operation("user_exists", 
                                 {"username": username}, 
                                 f"Utilisateur trouvé avec ID: {user_id}", True)
                return user_id
            else:
                self.log_operation("user_exists", 
                                 {"username": username}, 
                                 "Utilisateur non trouvé", False)
                self.logger.error(f"Utilisateur '{username}' n'existe pas dans la base Odoo")
                return None
                
        except Exception as e:
            self.log_operation("user_exists", 
                             {"username": username}, 
                             f"Erreur: {str(e)}", False)
            return None
    
    def update_user_info(self, user_id: int, new_email: str = None, new_password: str = None, **kwargs) -> bool:
        """
        II.1: Modifier les informations du compte utilisateur
        Met à jour l'email, le mot de passe ou d'autres données
        """
        try:
            if not self.uid:
                self.uid = self.authenticate()
                if not self.uid:
                    return False
            
            values = {}
            
            if new_email:
                values['email'] = new_email
                values['login'] = new_email  # Login est généralement l'email
            
            if new_password:
                values['password'] = new_password
            
            # Ajouter d'autres champs si fournis
            for key, value in kwargs.items():
                if value is not None:
                    values[key] = value
            
            if not values:
                self.logger.warning("Aucune valeur à mettre à jour")
                return False
            
            # Exécution de la mise à jour
            result = self.models.execute_kw(
                ODOO_DB, self.uid, ODOO_PASSWORD, 
                'res.users', 'write', 
                [[user_id], values]
            )
            
            if result:
                # Ne pas logger le mot de passe pour la sécurité
                log_values = {k: v for k, v in values.items() if k != 'password'}
                if 'password' in values:
                    log_values['password'] = '***MASQUÉ***'
                
                self.log_operation("update_user_info", 
                                 {"user_id": user_id, "values": log_values}, 
                                 "Informations utilisateur mises à jour", True)
                return True
            else:
                self.log_operation("update_user_info", 
                                 {"user_id": user_id, "values": values}, 
                                 "Échec de la mise à jour", False)
                return False
                
        except Exception as e:
            self.log_operation("update_user_info", 
                             {"user_id": user_id}, 
                             f"Erreur: {str(e)}", False)
            return False
    
    def get_user_groups(self, user_id: int) -> List[int]:
        """
        II.2: Récupère les groupes associés à un utilisateur
        """
        try:
            if not self.uid:
                self.uid = self.authenticate()
                if not self.uid:
                    return []
            
            groups = self.models.execute_kw(
                ODOO_DB, self.uid, ODOO_PASSWORD, 
                'res.users', 'read', 
                [user_id], {'fields': ['groups_id']}
            )
            
            group_ids = groups[0]['groups_id'] if groups else []
            
            self.log_operation("get_user_groups", 
                             {"user_id": user_id}, 
                             f"Groupes trouvés: {group_ids}", True)
            return group_ids
            
        except Exception as e:
            self.log_operation("get_user_groups", 
                             {"user_id": user_id}, 
                             f"Erreur: {str(e)}", False)
            return []
    
    def modify_user_groups(self, user_id: int, group_ids_to_add: List[int] = None, 
                          group_ids_to_remove: List[int] = None) -> bool:
        """
        II.2: Modifier les droits d'un compte existant
        Ajoute ou retire des groupes à un utilisateur
        """
        try:
            if not self.uid:
                self.uid = self.authenticate()
                if not self.uid:
                    return False
            
            if not group_ids_to_add:
                group_ids_to_add = []
            if not group_ids_to_remove:
                group_ids_to_remove = []
                
            if not group_ids_to_add and not group_ids_to_remove:
                self.logger.warning("Aucun groupe à ajouter ou retirer")
                return False
            
            # Récupérer les groupes actuels
            current_groups = self.get_user_groups(user_id)
            
            # Ajouter les groupes demandés
            for group_id in group_ids_to_add:
                if group_id not in current_groups:
                    current_groups.append(group_id)
            
            # Retirer les groupes demandés
            for group_id in group_ids_to_remove:
                if group_id in current_groups:
                    current_groups.remove(group_id)
            
            # Mise à jour des groupes de l'utilisateur
            # (6, 0, list) signifie "remplacer" la liste des groupes
            result = self.models.execute_kw(
                ODOO_DB, self.uid, ODOO_PASSWORD, 
                'res.users', 'write', 
                [[user_id], {'groups_id': [(6, 0, current_groups)]}]
            )
            
            if result:
                self.log_operation("modify_user_groups", 
                                 {"user_id": user_id, 
                                  "added": group_ids_to_add, 
                                  "removed": group_ids_to_remove}, 
                                 f"Groupes mis à jour: {current_groups}", True)
                return True
            else:
                self.log_operation("modify_user_groups", 
                                 {"user_id": user_id}, 
                                 "Échec de la modification des groupes", False)
                return False
                
        except Exception as e:
            self.log_operation("modify_user_groups", 
                             {"user_id": user_id}, 
                             f"Erreur: {str(e)}", False)
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """
        II.3: Supprimer un compte utilisateur existant
        """
        try:
            if not self.uid:
                self.uid = self.authenticate()
                if not self.uid:
                    return False
            
            # Récupérer les informations de l'utilisateur avant suppression
            user_info = self.models.execute_kw(
                ODOO_DB, self.uid, ODOO_PASSWORD, 
                'res.users', 'read', 
                [user_id], {'fields': ['name', 'login']}
            )
            
            if not user_info:
                self.log_operation("delete_user", 
                                 {"user_id": user_id}, 
                                 "Utilisateur non trouvé", False)
                return False
            
            # Suppression de l'utilisateur
            success = self.models.execute_kw(
                ODOO_DB, self.uid, ODOO_PASSWORD, 
                'res.users', 'unlink', 
                [[user_id]]
            )
            
            if success:
                self.log_operation("delete_user", 
                                 {"user_id": user_id, "user_info": user_info[0]}, 
                                 "Utilisateur supprimé avec succès", True)
                return True
            else:
                self.log_operation("delete_user", 
                                 {"user_id": user_id}, 
                                 "Échec de la suppression", False)
                return False
                
        except Exception as e:
            self.log_operation("delete_user", 
                             {"user_id": user_id}, 
                             f"Erreur: {str(e)}", False)
            return False
    
    def get_group_by_name(self, group_name: str) -> Optional[int]:
        """Fonction utilitaire pour récupérer l'ID d'un groupe par son nom"""
        try:
            if not self.uid:
                self.uid = self.authenticate()
                if not self.uid:
                    return None
            
            group_ids = self.models.execute_kw(
                ODOO_DB, self.uid, ODOO_PASSWORD, 
                'res.groups', 'search', 
                [[('name', 'ilike', group_name)]]
            )
            
            if group_ids:
                return group_ids[0]
            else:
                self.logger.warning(f"Groupe '{group_name}' non trouvé")
                return None
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche du groupe '{group_name}': {str(e)}")
            return None


def main():
    """Fonction de test pour la gestion des utilisateurs"""
    management = OdooUserManagement()
    
    print("="*60)
    print("TESTS DE GESTION DES UTILISATEURS ODOO")
    print("="*60)
    
    # Test 1: Recherche d'un utilisateur existant
    print("\n1. Test de recherche d'utilisateur:")
    username = "jean.dupont@iutcv.fr"
    user_id = management.user_exists(username)
    if user_id:
        print(f"✓ Utilisateur trouvé avec ID: {user_id}")
        
        # Test 2: Modification des informations utilisateur
        print("\n2. Test de modification des informations:")
        new_email = "jean.dupont.nouveau@iutcv.fr"
        success = management.update_user_info(user_id, new_email=new_email, name="Jean Dupont Modifié")
        if success:
            print("✓ Informations utilisateur mises à jour")
        else:
            print("✗ Échec de la mise à jour")
        
        # Test 3: Modification des groupes
        print("\n3. Test de modification des groupes:")
        current_groups = management.get_user_groups(user_id)
        print(f"Groupes actuels: {current_groups}")
        
        # Exemple: ajouter le groupe avec ID 1 et retirer le groupe avec ID 2 (si présent)
        success = management.modify_user_groups(user_id, group_ids_to_add=[1], group_ids_to_remove=[2])
        if success:
            print("✓ Groupes modifiés")
            new_groups = management.get_user_groups(user_id)
            print(f"Nouveaux groupes: {new_groups}")
        else:
            print("✗ Échec de la modification des groupes")
        
        # Test 4: Suppression (décommentez si vous voulez tester)
        # print("\n4. Test de suppression:")
        # print("ATTENTION: Ceci va supprimer l'utilisateur définitivement!")
        # confirm = input("Voulez-vous continuer? (oui/non): ")
        # if confirm.lower() == "oui":
        #     success = management.delete_user(user_id)
        #     if success:
        #         print("✓ Utilisateur supprimé")
        #     else:
        #         print("✗ Échec de la suppression")
        
    else:
        print(f"✗ Utilisateur '{username}' non trouvé")
    
    print("\n" + "="*60)
    print("TESTS TERMINÉS")
    print("="*60)


if __name__ == "__main__":
    main() 