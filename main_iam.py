#!/usr/bin/env python3
"""
Script principal simplifié du système IAM Odoo - Partie 1

Usage:
    python3 main_iam.py
    
Auteur: Système IAM Odoo
Date: 2025-05-28
"""

import sys
import os

def show_system_status():
    """Affiche le statut du système"""
    print("📊 STATUT DU SYSTÈME IAM ODOO - PARTIE 1")
    print("=" * 50)
    
    # Vérification des fichiers principaux
    files_to_check = [
        ("odoo_user_provisioning.py", "Système principal"),
        ("utilisateurs.csv", "Données utilisateurs"),
        ("config.py", "Configuration"),
        ("test_odoo_connection.py", "Tests système"),
        ("demo_iam_system.py", "Démonstration"),
        ("README.md", "Documentation")
    ]
    
    print("📁 Fichiers système:")
    all_present = True
    for file, description in files_to_check:
        if os.path.exists(file):
            print(f"   ✅ {file} - {description}")
        else:
            print(f"   ❌ {file} - MANQUANT")
            all_present = False
    
    # Vérification des dépendances Python
    print("\n📦 Dépendances Python:")
    dependencies = ['requests', 'pandas', 'csv', 'json', 'logging', 'smtplib']
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"   ✅ {dep}")
        except ImportError:
            print(f"   ❌ {dep} - NON INSTALLÉ")
            all_present = False
    
    print(f"\n🎯 Statut global: {'✅ SYSTÈME PRÊT' if all_present else '⚠️ CONFIGURATION INCOMPLÈTE'}")
    
    return all_present

def show_usage_guide():
    """Affiche le guide d'utilisation"""
    guide = """
🏗️  SYSTÈME DE PROVISIONNEMENT IAM POUR ODOO - PARTIE 1
=========================================================

📋 FONCTIONNALITÉS PRINCIPALES:
• Import automatique des utilisateurs depuis CSV
• Authentification sécurisée via API JSON-RPC Odoo
• Génération de mots de passe complexes
• Attribution automatique des rôles et permissions
• Notifications email avec identifiants
• Logging complet de toutes les opérations

🚀 COMMANDES DISPONIBLES:

1. DÉMONSTRATION (recommandé pour débuter):
   python3 demo_iam_system.py
   → Simule toutes les fonctionnalités sans Odoo

2. TESTS SYSTÈME:
   python3 test_odoo_connection.py
   → Valide la configuration et la connectivité

3. IMPORT RÉEL:
   python3 odoo_user_provisioning.py
   → Effectue l'import réel dans Odoo (nécessite Odoo actif)

📁 STRUCTURE DES FICHIERS:
• odoo_user_provisioning.py - Code principal du système
• utilisateurs.csv - Fichier d'exemple avec 8 utilisateurs
• config.py - Configuration Odoo et SMTP
• README.md - Documentation complète

⚙️  CONFIGURATION RAPIDE:
1. Éditez config.py avec vos paramètres Odoo
2. Adaptez utilisateurs.csv avec vos données
3. Configurez les paramètres SMTP (optionnel)

🔍 FORMAT CSV REQUIS:
nom,prenom,numero_utilisateur,login,email,adresse,droits

Exemple:
Dupont,Jean,1001,jean.dupont@iutcv.fr,jean.dupont@iutcv.fr,"123 Rue...",Administration

🏷️  RÔLES SUPPORTÉS:
• Administration - Accès administrateur complet
• Ventes - Gestion des ventes et clients
• Comptabilité - Gestion financière
• Ressources Humaines - Gestion du personnel

🔐 SÉCURITÉ:
• Mots de passe générés: 12 caractères minimum
• Complexité: majuscules, minuscules, chiffres, caractères spéciaux
• Authentification sécurisée via API Odoo
• Logs détaillés de toutes les opérations

📞 PROCHAINES ÉTAPES:
Ce système est la Partie 1 d'un projet complet en 3 parties:
• Partie 1: Provisionnement automatique (ACTUEL)
• Partie 2: Modification et gestion des utilisateurs
• Partie 3: Interface web et API REST
"""
    print(guide)

def main():
    """Fonction principale"""
    print("🎯 SYSTÈME IAM ODOO - PARTIE 1")
    print("=" * 40)
    
    # Vérification du statut
    status_ok = show_system_status()
    
    if not status_ok:
        print("\n⚠️  Certains composants sont manquants.")
        print("💡 Consultez README.md pour l'installation complète.")
        return
    
    print("\n" + "="*50)
    print("🎯 QUE VOULEZ-VOUS FAIRE?")
    print("="*50)
    print("1. 🎭 Voir la démonstration")
    print("2. 🧪 Lancer les tests")
    print("3. 🚀 Import réel dans Odoo")
    print("4. 📖 Guide d'utilisation")
    print("5. ❌ Quitter")
    
    try:
        choice = input("\nVotre choix (1-5): ").strip()
        
        if choice == "1":
            print("\n🎭 Lancement de la démonstration...")
            os.system("python3 demo_iam_system.py")
            
        elif choice == "2":
            print("\n🧪 Lancement des tests...")
            os.system("python3 test_odoo_connection.py")
            
        elif choice == "3":
            print("\n🚀 Import réel dans Odoo...")
            print("⚠️  ATTENTION: Cette opération créera des utilisateurs réels!")
            confirm = input("Continuer? (oui/non): ").lower()
            if confirm in ['oui', 'o', 'yes', 'y']:
                os.system("python3 odoo_user_provisioning.py")
            else:
                print("❌ Import annulé.")
                
        elif choice == "4":
            show_usage_guide()
            
        elif choice == "5":
            print("👋 Au revoir!")
            
        else:
            print("❌ Choix invalide.")
            
    except KeyboardInterrupt:
        print("\n\n👋 Programme interrompu par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")

if __name__ == "__main__":
    main()
