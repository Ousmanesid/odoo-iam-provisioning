#!/usr/bin/env python3
"""
Extension du système de provisionnement IAM pour Odoo avec connexion PostgreSQL
Cette extension permet une connexion directe à la base de données Odoo

Auteur: Système IAM Odoo Extended
Date: 2025-05-28
"""

import psycopg2
import hashlib
import base64
import os
from odoo_user_provisioning import OdooUserProvisioning
from typing import Optional, Dict, Any

class OdooUserProvisioningExtended(OdooUserProvisioning):
    """Extension de la classe OdooUserProvisioning avec support PostgreSQL"""
    
    def __init__(self, use_db_direct=False):
        super().__init__()
        self.use_db_direct = use_db_direct
        self.db_connection = None
        
    def connect_postgresql(self, host="localhost", port=5432, database="odoo", 
                          user="odoo", password="odoo"):
        """
        Établit une connexion directe à PostgreSQL pour Odoo
        Utile quand l'API JSON-RPC n'est pas disponible
        """
        try:
            self.db_connection = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            self.logger.info("Connexion PostgreSQL établie avec succès")
            return True
        except Exception as e:
            self.logger.error(f"Erreur de connexion PostgreSQL: {str(e)}")
            return False
    
    def hash_password(self, password: str) -> str:
        """
        Génère un hash de mot de passe compatible avec Odoo
        """
        # Odoo utilise PBKDF2 avec SHA512
        salt = os.urandom(16)
        iterations = 100000
        
        pwd_hash = hashlib.pbkdf2_hmac('sha512', 
                                      password.encode('utf-8'), 
                                      salt, 
                                      iterations)
        
        # Format Odoo: $pbkdf2-sha512$iterations$salt$hash
        encoded_salt = base64.b64encode(salt).decode('ascii')
        encoded_hash = base64.b64encode(pwd_hash).decode('ascii')
        
        return f"$pbkdf2-sha512${iterations}${encoded_salt}${encoded_hash}"
    
    def create_user_postgresql(self, user_data: Dict[str, str]) -> Optional[int]:
        """
        Crée un utilisateur directement dans PostgreSQL
        Alternative quand l'API JSON-RPC n'est pas disponible
        """
        if not self.db_connection:
            self.logger.error("Aucune connexion PostgreSQL active")
            return None
            
        try:
            cursor = self.db_connection.cursor()
            
            # Génération du mot de passe et hash
            password = self.generate_password()
            password_hash = self.hash_password(password)
            
            # Insertion dans res_users
            insert_query = """
            INSERT INTO res_users (
                name, login, email, password, active, 
                street, create_date, write_date
            ) VALUES (
                %s, %s, %s, %s, %s, %s, NOW(), NOW()
            ) RETURNING id
            """
            
            cursor.execute(insert_query, (
                f"{user_data['prenom']} {user_data['nom']}",
                user_data['email'],
                user_data['email'],
                password_hash,
                True,
                user_data.get('adresse', '')
            ))
            
            user_id = cursor.fetchone()[0]
            self.db_connection.commit()
            
            self.logger.info(f"Utilisateur créé via PostgreSQL - ID: {user_id}")
            
            # Envoyer email avec le mot de passe en clair
            user_data['password'] = password
            self.send_welcome_email(user_data, password)
            
            return user_id
            
        except Exception as e:
            self.logger.error(f"Erreur création utilisateur PostgreSQL: {str(e)}")
            if self.db_connection:
                self.db_connection.rollback()
            return None
    
    def get_group_id_postgresql(self, group_name: str) -> Optional[int]:
        """
        Recherche l'ID d'un groupe via PostgreSQL
        """
        if not self.db_connection:
            return None
            
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT id FROM res_groups WHERE name ILIKE %s LIMIT 1",
                (f"%{group_name}%",)
            )
            result = cursor.fetchone()
            return result[0] if result else None
            
        except Exception as e:
            self.logger.error(f"Erreur recherche groupe PostgreSQL: {str(e)}")
            return None
    
    def assign_permissions_postgresql(self, user_id: int, group_id: int) -> bool:
        """
        Assigne des permissions via PostgreSQL
        """
        if not self.db_connection:
            return False
            
        try:
            cursor = self.db_connection.cursor()
            
            # Insertion dans res_groups_users_rel
            cursor.execute(
                "INSERT INTO res_groups_users_rel (gid, uid) VALUES (%s, %s)",
                (group_id, user_id)
            )
            
            self.db_connection.commit()
            self.logger.info(f"Permissions assignées via PostgreSQL: user {user_id} -> group {group_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur assignation permissions PostgreSQL: {str(e)}")
            if self.db_connection:
                self.db_connection.rollback()
            return False
    
    def import_accounts_from_csv_extended(self, file_path: str):
        """
        Version étendue de l'import avec support PostgreSQL et JSON-RPC
        """
        self.logger.info(f"Import étendu depuis {file_path}")
        
        # Tentative de connexion JSON-RPC d'abord
        uid = self.authenticate()
        
        if not uid and self.use_db_direct:
            # Fallback vers PostgreSQL
            self.logger.info("API JSON-RPC indisponible, utilisation de PostgreSQL")
            if not self.connect_postgresql():
                self.logger.error("Impossible de se connecter via PostgreSQL")
                return
        
        import csv
        
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                total_users = 0
                successful_users = 0
                
                for row in reader:
                    total_users += 1
                    self.logger.info(f"Traitement: {row['prenom']} {row['nom']}")
                    
                    # Choix de la méthode de création
                    if uid:
                        # Via API JSON-RPC
                        user_id = self.create_user(uid, row)
                        if user_id and row.get('droits'):
                            group_id = self.get_group_id(uid, row['droits'])
                            if group_id:
                                self.assign_permissions(uid, user_id, group_id)
                    else:
                        # Via PostgreSQL direct
                        user_id = self.create_user_postgresql(row)
                        if user_id and row.get('droits'):
                            group_id = self.get_group_id_postgresql(row['droits'])
                            if group_id:
                                self.assign_permissions_postgresql(user_id, group_id)
                    
                    if user_id:
                        successful_users += 1
                
                self.logger.info(f"Import terminé: {successful_users}/{total_users} utilisateurs")
                
        except Exception as e:
            self.logger.error(f"Erreur import étendu: {str(e)}")
        
        finally:
            if self.db_connection:
                self.db_connection.close()


def main():
    """Test du système étendu"""
    print("=== Système de Provisionnement IAM Odoo Extended ===")
    
    # Test avec API JSON-RPC d'abord
    provisioning = OdooUserProvisioningExtended(use_db_direct=False)
    
    print("Test de connexion API JSON-RPC...")
    uid = provisioning.authenticate()
    
    if uid:
        print(f"✅ API JSON-RPC opérationnelle (UID: {uid})")
        provisioning.import_accounts_from_csv("utilisateurs.csv")
    else:
        print("❌ API JSON-RPC indisponible")
        print("💡 Pour utiliser PostgreSQL direct, configurez les paramètres de connexion")
        print("   et relancez avec use_db_direct=True")


if __name__ == "__main__":
    main()
