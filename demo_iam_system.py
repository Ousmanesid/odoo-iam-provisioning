#!/usr/bin/env python3
"""
Script de démonstration complète du système IAM Odoo
Inclut tous les tests et simulations sans connexion Odoo réelle

Auteur: Système IAM Odoo Demo
Date: 2025-05-28
"""

import json
import csv
import logging
from datetime import datetime
import random
import string

class OdooIAMDemo:
    """Classe de démonstration du système IAM"""
    
    def __init__(self):
        self.setup_logging()
        self.users_created = []
        self.groups_available = [
            {"id": 1, "name": "Administration", "category": "Administration"},
            {"id": 2, "name": "Ventes", "category": "Sales"},
            {"id": 3, "name": "Comptabilité", "category": "Accounting"},
            {"id": 4, "name": "Ressources Humaines", "category": "Human Resources"},
            {"id": 5, "name": "Utilisateur interne", "category": "Base"}
        ]
        
    def setup_logging(self):
        """Configuration du logging pour la démo"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('odoo_demo.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def generate_password(self, length=12):
        """Génère un mot de passe sécurisé"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(length))
        
        # Assurer la complexité
        if not any(c.isupper() for c in password):
            password = password[:-1] + random.choice(string.ascii_uppercase)
        if not any(c.islower() for c in password):
            password = password[:-1] + random.choice(string.ascii_lowercase)
        if not any(c.isdigit() for c in password):
            password = password[:-1] + random.choice(string.digits)
        if not any(c in "!@#$%^&*" for c in password):
            password = password[:-1] + random.choice("!@#$%^&*")
            
        return password
    
    def simulate_authentication(self):
        """Simule l'authentification à Odoo"""
        self.logger.info("🔐 Simulation de l'authentification Odoo...")
        # Simulation d'un délai réseau
        import time
        time.sleep(0.5)
        
        uid = random.randint(1000, 9999)
        self.logger.info(f"✅ Authentification simulée réussie - UID: {uid}")
        return uid
    
    def simulate_create_user(self, user_data):
        """Simule la création d'un utilisateur"""
        password = self.generate_password()
        user_id = random.randint(100, 999)
        
        user_info = {
            "id": user_id,
            "name": f"{user_data['prenom']} {user_data['nom']}",
            "email": user_data['email'],
            "password": password,
            "address": user_data.get('adresse', ''),
            "role": user_data.get('droits', 'Utilisateur'),
            "created_at": datetime.now().isoformat()
        }
        
        self.users_created.append(user_info)
        
        self.logger.info(f"👤 Utilisateur créé: {user_info['name']} (ID: {user_id})")
        self.logger.info(f"   📧 Email: {user_info['email']}")
        self.logger.info(f"   🔑 Mot de passe: {password}")
        
        return user_id, password
    
    def simulate_assign_role(self, user_id, role_name):
        """Simule l'attribution d'un rôle"""
        group = next((g for g in self.groups_available if g['name'] == role_name), None)
        
        if group:
            self.logger.info(f"🏷️  Rôle '{role_name}' assigné à l'utilisateur {user_id}")
            return True
        else:
            self.logger.warning(f"⚠️  Rôle '{role_name}' non trouvé")
            return False
    
    def simulate_email_notification(self, user_data, password):
        """Simule l'envoi d'email de bienvenue"""
        self.logger.info(f"📨 Email de bienvenue envoyé à {user_data['email']}")
        
        # Simulation du contenu de l'email
        email_content = f"""
        ════════════════════════════════════════
        📧 EMAIL DE BIENVENUE (SIMULATION)
        ════════════════════════════════════════
        
        Destinataire: {user_data['email']}
        Objet: Bienvenue - Votre compte Odoo
        
        Bonjour {user_data['prenom']} {user_data['nom']},
        
        Votre compte Odoo a été créé avec succès !
        
        🔗 URL de connexion: http://localhost:8069
        👤 Nom d'utilisateur: {user_data['email']}
        🔑 Mot de passe: {password}
        🏷️  Rôle: {user_data.get('droits', 'Non défini')}
        
        Nous vous recommandons de changer votre mot de passe
        lors de votre première connexion.
        
        Cordialement,
        L'équipe Administration
        ════════════════════════════════════════
        """
        
        print(email_content)
        return True
    
    def demo_csv_import(self, csv_file):
        """Démonstration complète de l'import CSV"""
        print("\n" + "="*60)
        print("🚀 DÉMONSTRATION DU SYSTÈME IAM ODOO")
        print("="*60)
        
        # 1. Authentification
        uid = self.simulate_authentication()
        
        # 2. Lecture du CSV
        self.logger.info(f"📂 Lecture du fichier CSV: {csv_file}")
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                users = list(reader)
                
            self.logger.info(f"📊 {len(users)} utilisateurs trouvés dans le CSV")
            
            # 3. Traitement de chaque utilisateur
            print("\n" + "-"*50)
            print("👥 CRÉATION DES UTILISATEURS")
            print("-"*50)
            
            for i, user in enumerate(users, 1):
                print(f"\n[{i}/{len(users)}] Traitement de {user['prenom']} {user['nom']}")
                
                # Création de l'utilisateur
                user_id, password = self.simulate_create_user(user)
                
                # Attribution du rôle
                if user.get('droits'):
                    self.simulate_assign_role(user_id, user['droits'])
                
                # Notification email
                self.simulate_email_notification(user, password)
                
                print("-" * 40)
            
            # 4. Résumé
            self.show_summary()
            
        except FileNotFoundError:
            self.logger.error(f"❌ Fichier {csv_file} non trouvé")
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du traitement: {str(e)}")
    
    def show_summary(self):
        """Affiche un résumé de l'opération"""
        print("\n" + "="*60)
        print("📋 RÉSUMÉ DE L'IMPORT")
        print("="*60)
        
        print(f"✅ Utilisateurs créés: {len(self.users_created)}")
        
        # Statistiques par rôle
        roles_count = {}
        for user in self.users_created:
            role = user.get('role', 'Non défini')
            roles_count[role] = roles_count.get(role, 0) + 1
        
        print("\n📊 Répartition par rôle:")
        for role, count in roles_count.items():
            print(f"   • {role}: {count} utilisateur(s)")
        
        print("\n👥 Liste des utilisateurs créés:")
        for user in self.users_created:
            print(f"   • {user['name']} ({user['email']}) - {user['role']}")
        
        print("\n🔧 Fonctionnalités démontrées:")
        print("   ✅ Authentification à Odoo")
        print("   ✅ Lecture et validation du CSV")
        print("   ✅ Génération de mots de passe sécurisés")
        print("   ✅ Création des comptes utilisateurs")
        print("   ✅ Attribution des rôles et permissions")
        print("   ✅ Envoi d'emails de bienvenue")
        print("   ✅ Logging complet des opérations")
        
        print(f"\n📝 Logs sauvegardés dans: odoo_demo.log")
    
    def show_available_groups(self):
        """Affiche les groupes disponibles"""
        print("\n🏷️  GROUPES DISPONIBLES DANS ODOO:")
        print("-" * 40)
        for group in self.groups_available:
            print(f"   • {group['name']} (Catégorie: {group['category']})")


def main():
    """Fonction principale de démonstration"""
    demo = OdooIAMDemo()
    
    # Affichage des groupes disponibles
    demo.show_available_groups()
    
    # Démonstration de l'import CSV
    demo.demo_csv_import("utilisateurs.csv")
    
    print("\n" + "="*60)
    print("✨ DÉMONSTRATION TERMINÉE")
    print("="*60)
    print("💡 Pour utiliser le système réel avec Odoo:")
    print("   1. Configurez les paramètres dans config.py")
    print("   2. Assurez-vous qu'Odoo est en cours d'exécution")
    print("   3. Lancez: python3 odoo_user_provisioning.py")


if __name__ == "__main__":
    main()
