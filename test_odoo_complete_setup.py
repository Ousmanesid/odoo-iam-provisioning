#!/usr/bin/env python3
"""
Script de test complet pour vérifier l'installation Odoo + PostgreSQL
"""

import psycopg2
import requests
import subprocess
import sys
import time

def test_postgresql_service():
    """Test du service PostgreSQL"""
    print("=== Test du service PostgreSQL ===")
    try:
        result = subprocess.run(['systemctl', 'is-active', 'postgresql'], 
                              capture_output=True, text=True)
        if result.returncode == 0 and 'active' in result.stdout:
            print("✅ Service PostgreSQL: ACTIF")
            return True
        else:
            print("❌ Service PostgreSQL: INACTIF")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test PostgreSQL: {e}")
        return False

def test_postgresql_connection():
    """Test de connexion à PostgreSQL"""
    print("\n=== Test de connexion PostgreSQL ===")
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='odoo_iam_db',
            user='odoo',
            port=5432
        )
        cursor = conn.cursor()
        
        # Test de version
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ Connexion PostgreSQL réussie")
        print(f"   Version: {version.split()[0]} {version.split()[1]}")
        
        # Test de permissions
        cursor.execute("SELECT current_user, current_database();")
        user, db = cursor.fetchone()
        print(f"   Utilisateur: {user}")
        print(f"   Base de données: {db}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion PostgreSQL: {e}")
        return False

def test_odoo_service():
    """Test du service Odoo"""
    print("\n=== Test du service Odoo ===")
    try:
        result = subprocess.run(['systemctl', 'is-active', 'odoo'], 
                              capture_output=True, text=True)
        if result.returncode == 0 and 'active' in result.stdout:
            print("✅ Service Odoo: ACTIF")
            
            # Test du port
            result = subprocess.run(['ss', '-tlnp'], capture_output=True, text=True)
            if ':8069' in result.stdout:
                print("✅ Port 8069: OUVERT")
                return True
            else:
                print("❌ Port 8069: FERMÉ")
                return False
        else:
            print("❌ Service Odoo: INACTIF")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test Odoo: {e}")
        return False

def test_odoo_web_interface():
    """Test de l'interface web Odoo"""
    print("\n=== Test de l'interface web Odoo ===")
    try:
        response = requests.get('http://localhost:8069', timeout=10)
        if response.status_code == 200:
            print("✅ Interface web Odoo: ACCESSIBLE")
            if 'odoo' in response.text.lower():
                print("✅ Page Odoo: CORRECTE")
                return True
            else:
                print("❌ Page Odoo: CONTENU INCORRECT")
                return False
        else:
            print(f"❌ Interface web Odoo: ERREUR {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test web: {e}")
        return False

def test_database_creation():
    """Test de création d'une base de données via Odoo"""
    print("\n=== Test de création de base de données ===")
    try:
        # Test de l'endpoint de gestion des bases
        response = requests.get('http://localhost:8069/web/database/manager', timeout=10)
        if response.status_code == 200:
            print("✅ Interface de gestion des bases: ACCESSIBLE")
            return True
        else:
            print(f"❌ Interface de gestion des bases: ERREUR {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test de gestion des bases: {e}")
        return False

def display_system_info():
    """Affichage des informations système"""
    print("\n=== Informations système ===")
    try:
        # Version d'Odoo
        result = subprocess.run(['odoo', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Version Odoo: {result.stdout.strip()}")
        
        # Version PostgreSQL
        result = subprocess.run(['sudo', '-u', 'postgres', 'psql', '-c', 'SELECT version();'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version_line = [line for line in result.stdout.split('\n') if 'PostgreSQL' in line]
            if version_line:
                print(f"Version PostgreSQL: {version_line[0].strip()}")
        
        # Espace disque
        result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                print(f"Espace disque: {lines[1].split()[3]} disponible")
        
    except Exception as e:
        print(f"Erreur lors de la récupération des infos système: {e}")

def main():
    """Fonction principale"""
    print("🚀 Test complet de l'installation Odoo + PostgreSQL")
    print("=" * 60)
    
    tests = [
        test_postgresql_service,
        test_postgresql_connection,
        test_odoo_service,
        test_odoo_web_interface,
        test_database_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Petite pause entre les tests
    
    print("\n" + "=" * 60)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Installation COMPLÈTE et FONCTIONNELLE!")
        print("\n📝 Prochaines étapes recommandées:")
        print("   1. Accéder à http://localhost:8069")
        print("   2. Créer une nouvelle base de données")
        print("   3. Configurer votre premier utilisateur admin")
        print("   4. Installer les modules Odoo souhaités")
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez la configuration.")
    
    display_system_info()
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
