#!/usr/bin/env python3
"""
Script principal du système de provisionnement IAM pour Odoo - Partie 1
Script unifié incluant toutes les fonctionnalités et modes de fonctionnement

Usage:
    python3 odoo_iam_complete.py --demo         # Mode démonstration
    python3 odoo_iam_complete.py --test         # Tests système
    python3 odoo_iam_complete.py --import       # Import réel (Odoo requis)
    python3 odoo_iam_complete.py --help         # Aide

Auteur: Système IAM Odoo - Partie 1
Date: 2025-05-28
"""

import sys
import argparse
import subprocess
import os

# Import conditionnel pour éviter les erreurs
try:
    from odoo_user_provisioning import OdooUserProvisioning
except ImportError:
    print("⚠️ Module odoo_user_provisioning non trouvé")
    OdooUserProvisioning = None

try:
    from demo_iam_system import OdooIAMDemo
except ImportError:
    print("⚠️ Module demo_iam_system non trouvé") 
    OdooIAMDemo = None

class OdooIAMManager:
    """Gestionnaire principal du système IAM Odoo"""
    
    def __init__(self):
        if OdooIAMDemo:
            self.demo = OdooIAMDemo()
        else:
            self.demo = None
            
        if OdooUserProvisioning:
            self.provisioning = OdooUserProvisioning()
        else:
            self.provisioning = None
    
    def run_demo(self):
        """Lance la démonstration complète"""
        print("🎭 MODE DÉMONSTRATION - Système IAM Odoo")
        print("=" * 60)
        self.demo.demo_csv_import("utilisateurs.csv")
    
    def run_tests(self):
        """Lance les tests du système"""
        print("🧪 MODE TESTS - Système IAM Odoo")
        print("=" * 60)
        subprocess.run([sys.executable, "test_odoo_connection.py"])
    
    def run_import(self):
        """Lance l'import réel"""
        print("🚀 MODE IMPORT RÉEL - Système IAM Odoo")
        print("=" * 60)
        print("⚠️  ATTENTION: Cette opération va créer des utilisateurs réels dans Odoo!")
        
        response = input("Voulez-vous continuer? (oui/non): ")
        if response.lower() in ['oui', 'o', 'yes', 'y']:
            self.provisioning.import_accounts_from_csv("utilisateurs.csv")
        else:
            print("❌ Import annulé par l'utilisateur")
    
    def show_help(self):
        """Affiche l'aide du système"""
        help_text = """
🏗️  SYSTÈME DE PROVISIONNEMENT IAM POUR ODOO - PARTIE 1
=========================================================

📋 DESCRIPTION:
Ce système automatise la gestion des utilisateurs Odoo via:
- Import depuis fichiers CSV
- Création automatique des comptes
- Attribution des rôles et permissions
- Génération de mots de passe sécurisés
- Notifications email
- Logging complet des opérations

🚀 MODES D'UTILISATION:

1. MODE DÉMONSTRATION (--demo)
   • Simule toutes les fonctionnalités sans Odoo
   • Parfait pour comprendre le fonctionnement
   • Génère des logs de démonstration

2. MODE TESTS (--test)
   • Valide la configuration et les dépendances
   • Teste la connectivité Odoo
   • Vérifie la structure des fichiers CSV

3. MODE IMPORT RÉEL (--import)
   • Effectue l'import réel dans Odoo
   • Nécessite une instance Odoo opérationnelle
   • Crée les utilisateurs et assigne les permissions

📁 FICHIERS PRINCIPAUX:
• odoo_user_provisioning.py - Système principal
• utilisateurs.csv - Données d'exemple
• config.py - Configuration système
• odoo_provisioning.log - Logs d'exécution

⚙️  CONFIGURATION:
1. Éditez config.py avec vos paramètres Odoo
2. Configurez les paramètres SMTP pour les emails
3. Adaptez utilisateurs.csv avec vos données

🔧 PRÉREQUIS:
• Python 3.8+
• Packages: requests, pandas
• Odoo 14+ (pour le mode import réel)

📖 EXEMPLES:
    python3 odoo_iam_complete.py --demo    # Démonstration
    python3 odoo_iam_complete.py --test    # Tests
    python3 odoo_iam_complete.py --import  # Import réel

🔍 STRUCTURE CSV REQUISE:
nom,prenom,numero_utilisateur,login,email,adresse,droits

🏷️  RÔLES SUPPORTÉS:
• Administration
• Ventes  
• Comptabilité
• Ressources Humaines

📞 SUPPORT:
Ce système fait partie du projet IAM Odoo en 3 parties:
- Partie 1: Provisionnement automatique (ACTUEL)
- Partie 2: Modification et gestion (À VENIR)
- Partie 3: API REST et interface web (À VENIR)
        """
        print(help_text)
    
    def show_status(self):
        """Affiche le statut du système"""
        print("📊 STATUT DU SYSTÈME IAM ODOO")
        print("=" * 40)
        
        # Vérification des fichiers
        import os
        files_to_check = [
            "odoo_user_provisioning.py",
            "utilisateurs.csv", 
            "config.py",
            "test_odoo_connection.py"
        ]
        
        print("📁 Fichiers système:")
        for file in files_to_check:
            if os.path.exists(file):
                print(f"   ✅ {file}")
            else:
                print(f"   ❌ {file} - MANQUANT")
        
        # Vérification des dépendances
        print("\n📦 Dépendances Python:")
        try:
            import requests
            print("   ✅ requests")
        except ImportError:
            print("   ❌ requests - NON INSTALLÉ")
        
        try:
            import pandas
            print("   ✅ pandas")
        except ImportError:
            print("   ❌ pandas - NON INSTALLÉ")
        
        # Test de connexion Odoo (rapide)
        print("\n🔗 Connectivité Odoo:")
        uid = self.provisioning.authenticate()
        if uid:
            print(f"   ✅ Connexion OK (UID: {uid})")
        else:
            print("   ❌ Connexion impossible")
            print("     → Vérifiez que Odoo est démarré")
            print("     → Vérifiez la configuration dans config.py")


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Système de provisionnement IAM pour Odoo - Partie 1",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--demo', action='store_true', 
                       help='Mode démonstration (sans Odoo)')
    parser.add_argument('--test', action='store_true',
                       help='Lance les tests du système')
    parser.add_argument('--import', action='store_true',
                       help='Import réel dans Odoo')
    parser.add_argument('--status', action='store_true',
                       help='Affiche le statut du système')
    
    args = parser.parse_args()
    
    manager = OdooIAMManager()
    
    if args.demo:
        manager.run_demo()
    elif args.test:
        manager.run_tests()
    elif getattr(args, 'import'):
        manager.run_import()
    elif args.status:
        manager.show_status()
    else:
        manager.show_help()


if __name__ == "__main__":
    main()
