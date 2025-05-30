#!/usr/bin/env python3
"""
Script de test pour vérifier la connexion à Odoo et les fonctionnalités de base

Ce script teste:
1. La connexion à Odoo
2. La lecture des groupes existants  
3. La structure du fichier CSV
4. Les fonctions de base sans créer d'utilisateurs
"""

import json
import csv
import requests
from odoo_user_provisioning import OdooUserProvisioning

def test_odoo_connection():
    """Test de connexion à Odoo"""
    print("🔍 Test de connexion à Odoo...")
    
    provisioning = OdooUserProvisioning()
    uid = provisioning.authenticate()
    
    if uid:
        print(f"✅ Connexion réussie - UID: {uid}")
        return True
    else:
        print("❌ Échec de la connexion")
        return False

def test_csv_structure():
    """Test de la structure du fichier CSV"""
    print("\n🔍 Vérification de la structure du fichier CSV...")
    
    required_fields = ['nom', 'prenom', 'numero_utilisateur', 'login', 'email', 'adresse', 'droits']
    
    try:
        with open('utilisateurs.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            
            print(f"Champs trouvés: {fieldnames}")
            
            # Vérification des champs requis
            missing_fields = [field for field in required_fields if field not in fieldnames]
            if missing_fields:
                print(f"❌ Champs manquants: {missing_fields}")
                return False
            
            print("✅ Structure CSV correcte")
            
            # Affichage des premiers utilisateurs
            users = list(reader)
            print(f"📊 {len(users)} utilisateurs trouvés dans le CSV")
            
            for i, user in enumerate(users[:3]):
                print(f"   {i+1}. {user['prenom']} {user['nom']} - {user['email']} - {user['droits']}")
            
            if len(users) > 3:
                print(f"   ... et {len(users)-3} autres")
                
            return True
            
    except FileNotFoundError:
        print("❌ Fichier utilisateurs.csv non trouvé")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du CSV: {e}")
        return False

def test_groups_retrieval():
    """Test de récupération des groupes Odoo"""
    print("\n🔍 Test de récupération des groupes...")
    
    provisioning = OdooUserProvisioning()
    groups = provisioning.list_existing_groups()
    
    if groups:
        print(f"✅ {len(groups)} groupes trouvés dans Odoo:")
        
        # Groupes par catégorie
        categories = {}
        for group in groups:
            category = group.get('category_id', [False, 'Sans catégorie'])[1] if group.get('category_id') else 'Sans catégorie'
            if category not in categories:
                categories[category] = []
            categories[category].append(group['name'])
        
        for category, group_names in list(categories.items())[:5]:  # Afficher 5 catégories max
            print(f"   📁 {category}:")
            for name in group_names[:3]:  # 3 groupes max par catégorie
                print(f"      - {name}")
            if len(group_names) > 3:
                print(f"      ... et {len(group_names)-3} autres")
        
        return True
    else:
        print("❌ Aucun groupe trouvé ou erreur de connexion")
        return False

def test_group_search():
    """Test de recherche de groupes spécifiques"""
    print("\n🔍 Test de recherche de groupes spécifiques...")
    
    provisioning = OdooUserProvisioning()
    uid = provisioning.authenticate()
    
    if not uid:
        print("❌ Impossible de s'authentifier")
        return False
    
    # Test avec quelques groupes communs
    test_groups = ['Administration', 'Sales Manager', 'User', 'Employee']
    
    for group_name in test_groups:
        group_id = provisioning.get_group_id(uid, group_name)
        if group_id:
            print(f"   ✅ '{group_name}' trouvé (ID: {group_id})")
        else:
            print(f"   ⚠️  '{group_name}' non trouvé")
    
    return True

def test_password_generation():
    """Test de génération de mots de passe"""
    print("\n🔍 Test de génération de mots de passe...")
    
    provisioning = OdooUserProvisioning()
    
    print("Génération de 3 mots de passe de test:")
    for i in range(3):
        password = provisioning.generate_password()
        print(f"   {i+1}. {password}")
    
    print("✅ Génération de mots de passe fonctionnelle")
    return True

def main():
    """Fonction principale de test"""
    print("🧪 TESTS DU SYSTÈME DE PROVISIONNEMENT ODOO")
    print("=" * 60)
    
    tests = [
        ("Connexion Odoo", test_odoo_connection),
        ("Structure CSV", test_csv_structure), 
        ("Récupération des groupes", test_groups_retrieval),
        ("Recherche de groupes", test_group_search),
        ("Génération de mots de passe", test_password_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur lors du test '{test_name}': {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print("\n📋 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{len(tests)} tests réussis")
    
    if passed == len(tests):
        print("🎉 Tous les tests sont passés ! Le système est prêt.")
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez la configuration Odoo.")
        
    print("\n💡 Pour exécuter l'import réel:")
    print("   python odoo_user_provisioning.py")

if __name__ == "__main__":
    main()
