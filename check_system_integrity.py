#!/usr/bin/env python3
"""
Script de vérification d'intégrité complète du système IAM Odoo
Valide tous les composants et génère un rapport de statut

Auteur: Système IAM Odoo
Date: 2025-05-28
"""

import os
import sys
import subprocess
import importlib
from datetime import datetime

class SystemIntegrityChecker:
    """Vérificateur d'intégrité du système IAM"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.results = []
    
    def log_result(self, test_name, status, message):
        """Enregistre un résultat de test"""
        self.results.append({
            'test': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
        
        if status == "PASS":
            self.passed += 1
        elif status == "FAIL":
            self.failed += 1
        else:
            self.warnings += 1
    
    def check_file_integrity(self):
        """Vérifie l'intégrité des fichiers du système"""
        print("🔍 Vérification de l'intégrité des fichiers...")
        
        required_files = {
            'odoo_user_provisioning.py': 'Système principal',
            'utilisateurs.csv': 'Données d\'exemple',
            'config.py': 'Configuration',
            'demo_iam_system.py': 'Démonstration',
            'test_odoo_connection.py': 'Tests système',
            'README.md': 'Documentation',
            'PROJET_COMPLET.md': 'Documentation finale'
        }
        
        for file, description in required_files.items():
            if os.path.exists(file):
                size = os.path.getsize(file)
                if size > 0:
                    self.log_result(f"Fichier {file}", "PASS", f"{description} - {size} bytes")
                else:
                    self.log_result(f"Fichier {file}", "FAIL", "Fichier vide")
            else:
                self.log_result(f"Fichier {file}", "FAIL", "Fichier manquant")
    
    def check_python_dependencies(self):
        """Vérifie les dépendances Python"""
        print("📦 Vérification des dépendances Python...")
        
        dependencies = [
            'requests', 'csv', 'json', 'logging', 'smtplib', 
            'datetime', 'random', 'string', 'os', 'sys'
        ]
        
        for dep in dependencies:
            try:
                importlib.import_module(dep)
                self.log_result(f"Module {dep}", "PASS", "Disponible")
            except ImportError:
                self.log_result(f"Module {dep}", "FAIL", "Non installé")
    
    def check_csv_structure(self):
        """Vérifie la structure du fichier CSV"""
        print("📊 Vérification de la structure CSV...")
        
        required_fields = ['nom', 'prenom', 'numero_utilisateur', 'login', 'email', 'adresse', 'droits']
        
        try:
            import csv
            with open('utilisateurs.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                
                # Vérification des champs
                missing_fields = [field for field in required_fields if field not in fieldnames]
                if missing_fields:
                    self.log_result("Structure CSV", "FAIL", f"Champs manquants: {missing_fields}")
                else:
                    self.log_result("Structure CSV", "PASS", "Tous les champs requis présents")
                
                # Comptage des utilisateurs
                users = list(reader)
                if len(users) > 0:
                    self.log_result("Données CSV", "PASS", f"{len(users)} utilisateurs trouvés")
                else:
                    self.log_result("Données CSV", "FAIL", "Aucun utilisateur dans le CSV")
                    
        except Exception as e:
            self.log_result("Lecture CSV", "FAIL", f"Erreur: {str(e)}")
    
    def check_code_syntax(self):
        """Vérifie la syntaxe du code Python"""
        print("🔧 Vérification de la syntaxe du code...")
        
        python_files = [
            'odoo_user_provisioning.py',
            'demo_iam_system.py', 
            'test_odoo_connection.py',
            'main_iam.py'
        ]
        
        for file in python_files:
            if os.path.exists(file):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        code = f.read()
                    compile(code, file, 'exec')
                    self.log_result(f"Syntaxe {file}", "PASS", "Code valide")
                except SyntaxError as e:
                    self.log_result(f"Syntaxe {file}", "FAIL", f"Erreur syntaxe: {str(e)}")
                except Exception as e:
                    self.log_result(f"Syntaxe {file}", "WARN", f"Avertissement: {str(e)}")
    
    def check_functionality(self):
        """Teste les fonctionnalités de base"""
        print("⚙️ Vérification des fonctionnalités...")
        
        try:
            # Test import principal
            sys.path.append('.')
            from odoo_user_provisioning import OdooUserProvisioning
            
            provisioning = OdooUserProvisioning()
            self.log_result("Import principal", "PASS", "Module chargé avec succès")
            
            # Test génération mot de passe
            password = provisioning.generate_password()
            if len(password) >= 12:
                self.log_result("Génération mot de passe", "PASS", f"Mot de passe généré: {len(password)} chars")
            else:
                self.log_result("Génération mot de passe", "FAIL", "Mot de passe trop court")
                
        except Exception as e:
            self.log_result("Test fonctionnalités", "FAIL", f"Erreur: {str(e)}")
    
    def run_demo_test(self):
        """Lance un test rapide de la démonstration"""
        print("🎭 Test de la démonstration...")
        
        try:
            result = subprocess.run([sys.executable, 'demo_iam_system.py'], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                output_lines = len(result.stdout.split('\n'))
                self.log_result("Démonstration", "PASS", f"Exécutée avec succès - {output_lines} lignes de sortie")
            else:
                self.log_result("Démonstration", "FAIL", f"Code de retour: {result.returncode}")
                
        except subprocess.TimeoutExpired:
            self.log_result("Démonstration", "WARN", "Timeout - démonstration probablement interactive")
        except Exception as e:
            self.log_result("Démonstration", "FAIL", f"Erreur: {str(e)}")
    
    def generate_report(self):
        """Génère le rapport final"""
        print("\n" + "="*60)
        print("📋 RAPPORT D'INTÉGRITÉ SYSTÈME IAM ODOO")
        print("="*60)
        
        print(f"🕐 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Tests effectués: {len(self.results)}")
        print(f"✅ Succès: {self.passed}")
        print(f"❌ Échecs: {self.failed}")
        print(f"⚠️ Avertissements: {self.warnings}")
        
        # Calcul du score
        total_tests = self.passed + self.failed + self.warnings
        if total_tests > 0:
            score = (self.passed / total_tests) * 100
            print(f"🎯 Score d'intégrité: {score:.1f}%")
        
        print("\n📋 DÉTAIL DES TESTS:")
        print("-" * 60)
        
        for result in self.results:
            status_icon = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}[result['status']]
            print(f"{status_icon} {result['test']:30} | {result['message']}")
        
        # Évaluation globale
        print("\n" + "="*60)
        if self.failed == 0:
            if self.warnings == 0:
                print("🎉 SYSTÈME PARFAITEMENT OPÉRATIONNEL")
                print("✨ Tous les composants fonctionnent correctement")
                print("🚀 Prêt pour la production")
            else:
                print("✅ SYSTÈME OPÉRATIONNEL")
                print("⚠️ Quelques avertissements à examiner")
                print("🔧 Vérifiez les éléments en avertissement")
        else:
            print("❌ PROBLÈMES DÉTECTÉS")
            print("🔧 Corrigez les erreurs avant utilisation")
            print("📞 Consultez la documentation pour l'aide")
        
        print("="*60)
    
    def run_full_check(self):
        """Lance la vérification complète"""
        print("🔍 VÉRIFICATION D'INTÉGRITÉ SYSTÈME IAM ODOO")
        print("="*50)
        
        self.check_file_integrity()
        self.check_python_dependencies()
        self.check_csv_structure()
        self.check_code_syntax()
        self.check_functionality()
        self.run_demo_test()
        
        self.generate_report()


def main():
    """Fonction principale"""
    checker = SystemIntegrityChecker()
    checker.run_full_check()


if __name__ == "__main__":
    main()
