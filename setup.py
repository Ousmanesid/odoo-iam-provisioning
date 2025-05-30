#!/usr/bin/env python3
"""
Installation et configuration des dépendances pour le système de provisionnement Odoo

Ce script installe les packages nécessaires et vérifie la configuration.
"""

import subprocess
import sys
import importlib

def install_package(package):
    """Installe un package Python via pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installé avec succès")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Erreur lors de l'installation de {package}")
        return False

def check_package(package):
    """Vérifie si un package est installé"""
    try:
        importlib.import_module(package)
        print(f"✅ {package} est déjà installé")
        return True
    except ImportError:
        print(f"⚠️  {package} n'est pas installé")
        return False

def main():
    print("🔧 Installation des dépendances pour le provisionnement Odoo")
    print("=" * 60)
    
    # Liste des packages requis
    required_packages = [
        "requests",
        "pandas"
    ]
    
    # Vérification et installation des packages
    for package in required_packages:
        if not check_package(package):
            print(f"📦 Installation de {package}...")
            install_package(package)
    
    print("\n🎯 Vérification de la configuration...")
    
    # Vérification du fichier CSV
    try:
        with open("utilisateurs.csv", "r") as f:
            lines = f.readlines()
            print(f"✅ Fichier utilisateurs.csv trouvé ({len(lines)-1} utilisateurs)")
    except FileNotFoundError:
        print("❌ Fichier utilisateurs.csv non trouvé")
    
    # Création du fichier de configuration si nécessaire
    try:
        import config
        print("✅ Fichier config.py trouvé")
    except ImportError:
        print("⚠️  Fichier config.py non trouvé - utilisation de la configuration par défaut")
        print("   Copiez config_template.py vers config.py et adaptez les valeurs")
    
    print("\n🚀 Installation terminée !")
    print("=" * 60)
    print("Pour utiliser le système :")
    print("1. Assurez-vous qu'Odoo est en cours d'exécution")
    print("2. Adaptez la configuration dans config.py si nécessaire") 
    print("3. Exécutez: python odoo_user_provisioning.py")

if __name__ == "__main__":
    main()
