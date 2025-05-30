#!/usr/bin/env python3
"""
Système de provisionnement IAM pour Odoo
Partie 1: Import automatique des utilisateurs depuis un fichier CSV

Auteur: Système IAM Odoo
Date: 2025-05-28
"""

import csv
import requests
import random
import string
import json
import logging
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any, List

# Configuration Odoo
ODOO_URL = "http://localhost:8069"
ODOO_DB = "odoo_db"
ODOO_USERNAME = "admin"
ODOO_PASSWORD = "admin"  # Mot de passe par défaut Odoo

# Configuration Email (à adapter selon votre serveur SMTP)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your-email@gmail.com"
SMTP_PASSWORD = "your-password"

# Configuration du logging
LOG_FILE = "odoo_provisioning.log"

class OdooUserProvisioning:
    """Classe principale pour le provisionnement des utilisateurs Odoo"""
    
    def __init__(self):
        self.setup_logging()
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
        """
        I.1: Connexion à la base Odoo via l'API RPC
        Authentifie l'utilisateur et retourne l'UID de session
        """
        try:
            url = f"{ODOO_URL}/jsonrpc"
            headers = {'Content-Type': 'application/json'}
            auth_data = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "common",
                    "method": "authenticate",
                    "args": [ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {}]
                },
                "id": 1
            }
            
            response = requests.post(url, json=auth_data, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            if result.get("result"):
                self.uid = result["result"]
                self.log_operation("authenticate", 
                                 {"db": ODOO_DB, "user": ODOO_USERNAME}, 
                                 f"UID: {self.uid}", True)
                return self.uid
            else:
                error_msg = result.get("error", "Authentification échouée")
                self.log_operation("authenticate", 
                                 {"db": ODOO_DB, "user": ODOO_USERNAME}, 
                                 error_msg, False)
                return None
                
        except requests.exceptions.RequestException as e:
            self.log_operation("authenticate", 
                             {"db": ODOO_DB, "user": ODOO_USERNAME}, 
                             f"Erreur de connexion: {str(e)}", False)
            return None
        except Exception as e:
            self.log_operation("authenticate", 
                             {"db": ODOO_DB, "user": ODOO_USERNAME}, 
                             f"Erreur inattendue: {str(e)}", False)
            return None
    
    def generate_password(self, length: int = 12) -> str:
        """
        I.3: Génération du mot de passe
        Génère un mot de passe aléatoire sécurisé
        """
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
    
    def create_user(self, uid: int, user: Dict[str, str]) -> Optional[int]:
        """
        I.2: Création d'un utilisateur
        Crée un nouvel utilisateur dans Odoo avec mot de passe généré
        """
        try:
            # Génération du mot de passe
            password = self.generate_password()
            user['password'] = password
            
            url = f"{ODOO_URL}/jsonrpc"
            headers = {'Content-Type': 'application/json'}
            create_user_data = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute_kw",
                    "args": [ODOO_DB, uid, ODOO_PASSWORD, "res.users", "create", [{
                        "name": f"{user['prenom']} {user['nom']}",
                        "login": user['email'],
                        "email": user['email'],
                        "password": password,
                        "active": True,
                        "street": user.get('adresse', ''),
                        "employee_id": user.get('numero_utilisateur')
                    }]]
                },
                "id": 2
            }
            
            response = requests.post(url, json=create_user_data, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            if result.get("result"):
                user_id = result["result"]
                user_data = {k: v for k, v in user.items() if k != 'password'}  # Ne pas logger le mot de passe
                self.log_operation("create_user", user_data, f"User ID: {user_id}", True)
                
                # Envoyer email avec les identifiants
                self.send_welcome_email(user, password)
                
                return user_id
            else:
                error_msg = result.get("error", "Création utilisateur échouée")
                self.log_operation("create_user", user, error_msg, False)
                return None
                
        except Exception as e:
            self.log_operation("create_user", user, f"Erreur: {str(e)}", False)
            return None
    
    def get_group_id(self, uid: int, group_name: str) -> Optional[int]:
        """
        I.4: Recherche de l'ID d'un groupe Odoo par son nom
        """
        try:
            url = f"{ODOO_URL}/jsonrpc"
            headers = {'Content-Type': 'application/json'}
            search_data = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute_kw",
                    "args": [ODOO_DB, uid, ODOO_PASSWORD, "res.groups", "search", 
                            [[("name", "ilike", group_name)]]]
                },
                "id": 3
            }
            
            response = requests.post(url, json=search_data, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            if result.get("result") and len(result["result"]) > 0:
                group_id = result["result"][0]
                self.log_operation("get_group_id", 
                                 {"group_name": group_name}, 
                                 f"Group ID: {group_id}", True)
                return group_id
            else:
                self.log_operation("get_group_id", 
                                 {"group_name": group_name}, 
                                 "Groupe non trouvé", False)
                return None
                
        except Exception as e:
            self.log_operation("get_group_id", 
                             {"group_name": group_name}, 
                             f"Erreur: {str(e)}", False)
            return None
    
    def assign_permissions(self, uid: int, user_id: int, group_id: int) -> bool:
        """
        I.4: Attribution des droits à un utilisateur
        Assigne un utilisateur à un groupe (rôle)
        """
        try:
            url = f"{ODOO_URL}/jsonrpc"
            headers = {'Content-Type': 'application/json'}
            assign_data = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute_kw",
                    "args": [ODOO_DB, uid, ODOO_PASSWORD, "res.users", "write", 
                            [[user_id], {"groups_id": [(4, group_id)]}]]
                },
                "id": 4
            }
            
            response = requests.post(url, json=assign_data, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            if result.get("result"):
                self.log_operation("assign_permissions", 
                                 {"user_id": user_id, "group_id": group_id}, 
                                 "Permissions assignées avec succès", True)
                return True
            else:
                error_msg = result.get("error", "Échec de l'assignation des permissions")
                self.log_operation("assign_permissions", 
                                 {"user_id": user_id, "group_id": group_id}, 
                                 error_msg, False)
                return False
                
        except Exception as e:
            self.log_operation("assign_permissions", 
                             {"user_id": user_id, "group_id": group_id}, 
                             f"Erreur: {str(e)}", False)
            return False
    
    def send_welcome_email(self, user: Dict[str, str], password: str):
        """
        Envoie un email de bienvenue à l'utilisateur avec ses identifiants
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = SMTP_USER
            msg['To'] = user['email']
            msg['Subject'] = "Bienvenue - Votre compte Odoo a été créé"
            
            body = f"""
            Bonjour {user['prenom']} {user['nom']},
            
            Votre compte Odoo a été créé avec succès !
            
            Voici vos identifiants de connexion :
            - URL : {ODOO_URL}
            - Nom d'utilisateur : {user['email']}
            - Mot de passe : {password}
            - Rôle : {user.get('droits', 'Non défini')}
            
            Nous vous recommandons de changer votre mot de passe lors de votre première connexion.
            
            Cordialement,
            L'équipe administration
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            text = msg.as_string()
            server.sendmail(SMTP_USER, user['email'], text)
            server.quit()
            
            self.logger.info(f"Email envoyé à {user['email']}")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'envoi de l'email à {user['email']}: {str(e)}")
    
    def import_accounts_from_csv(self, file_path: str):
        """
        I.4: Intégration des différentes fonctions pour implémenter le script d'import automatique
        Fonction principale qui importe tous les utilisateurs depuis un fichier CSV
        """
        self.logger.info(f"Début de l'import depuis {file_path}")
        
        # Authentification
        uid = self.authenticate()
        if not uid:
            self.logger.error("Échec de l'authentification à Odoo")
            return
        
        self.logger.info("Authentification réussie")
        
        try:
            # Lecture du fichier CSV
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                total_users = 0
                successful_users = 0
                
                for row in reader:
                    total_users += 1
                    self.logger.info(f"Traitement de l'utilisateur: {row['prenom']} {row['nom']}")
                    
                    # Création de l'utilisateur
                    user_id = self.create_user(uid, row)
                    if user_id:
                        self.logger.info(f"Utilisateur créé avec ID: {user_id}")
                        
                        # Attribution des permissions si un rôle est défini
                        if row.get('droits'):
                            group_id = self.get_group_id(uid, row['droits'])
                            if group_id:
                                if self.assign_permissions(uid, user_id, group_id):
                                    self.logger.info(f"Utilisateur {row['prenom']} {row['nom']} créé avec le rôle {row['droits']}")
                                    successful_users += 1
                                else:
                                    self.logger.error(f"Échec de l'assignation du rôle pour {row['prenom']} {row['nom']}")
                            else:
                                self.logger.warning(f"Groupe {row['droits']} introuvable pour {row['prenom']} {row['nom']}")
                                successful_users += 1  # Utilisateur créé mais sans rôle
                        else:
                            self.logger.info(f"Aucun rôle défini pour {row['prenom']} {row['nom']}")
                            successful_users += 1
                    else:
                        self.logger.error(f"Échec de la création de l'utilisateur {row['prenom']} {row['nom']}")
                
                # Résumé de l'import
                self.logger.info(f"Import terminé: {successful_users}/{total_users} utilisateurs créés avec succès")
                self.log_operation("import_accounts_from_csv", 
                                 {"file": file_path, "total": total_users}, 
                                 f"Succès: {successful_users}/{total_users}", 
                                 successful_users > 0)
                
        except FileNotFoundError:
            self.logger.error(f"Fichier {file_path} non trouvé")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'import: {str(e)}")
    
    def list_existing_groups(self) -> List[Dict]:
        """
        Fonction utilitaire pour lister les groupes existants dans Odoo
        """
        uid = self.authenticate()
        if not uid:
            return []
        
        try:
            url = f"{ODOO_URL}/jsonrpc"
            headers = {'Content-Type': 'application/json'}
            search_data = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "object",
                    "method": "execute_kw",
                    "args": [ODOO_DB, uid, ODOO_PASSWORD, "res.groups", "search_read", 
                            [[]], {"fields": ["name", "category_id"]}]
                },
                "id": 5
            }
            
            response = requests.post(url, json=search_data, headers=headers)
            result = response.json()
            
            if result.get("result"):
                return result["result"]
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des groupes: {str(e)}")
            return []


def main():
    """Fonction principale pour tester le système"""
    provisioning = OdooUserProvisioning()
    
    # Lister les groupes existants (optionnel)
    print("Groupes existants dans Odoo:")
    groups = provisioning.list_existing_groups()
    for group in groups[:10]:  # Afficher les 10 premiers
        print(f"- {group['name']}")
    
    print("\n" + "="*50)
    print("IMPORT DES UTILISATEURS")
    print("="*50)
    
    # Import des utilisateurs
    csv_file = "utilisateurs.csv"
    provisioning.import_accounts_from_csv(csv_file)


if __name__ == "__main__":
    main()
