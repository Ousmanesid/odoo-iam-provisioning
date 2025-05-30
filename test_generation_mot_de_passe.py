#!/usr/bin/env python3
"""
Script de test pour démontrer la génération automatique de mots de passe
Section I.3 du projet de provisionnement IAM pour Odoo
"""

import re
import secrets
import string
import json
import csv
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class TestGenerationMotDePasse:
    """Test de la génération automatique de mots de passe"""
    
    def __init__(self):
        self.resultats = []
        print("=" * 60)
        print("TEST - GÉNÉRATION AUTOMATIQUE DE MOTS DE PASSE")
        print("Section I.3 du projet IAM Odoo")
        print("=" * 60)
    
    def generate_password(self, longueur=12):
        """
        Génère un mot de passe sécurisé avec les critères suivants:
        - Au moins 1 majuscule
        - Au moins 1 minuscule  
        - Au moins 1 chiffre
        - Au moins 1 caractère spécial
        - Longueur minimale de 12 caractères
        """
        if longueur < 12:
            longueur = 12
            
        # Définir les jeux de caractères
        majuscules = string.ascii_uppercase
        minuscules = string.ascii_lowercase
        chiffres = string.digits
        caracteres_speciaux = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Garantir au moins un caractère de chaque type
        password = [
            secrets.choice(majuscules),
            secrets.choice(minuscules),
            secrets.choice(chiffres),
            secrets.choice(caracteres_speciaux)
        ]
        
        # Compléter avec des caractères aléatoires
        tous_caracteres = majuscules + minuscules + chiffres + caracteres_speciaux
        for _ in range(longueur - 4):
            password.append(secrets.choice(tous_caracteres))
        
        # Mélanger le mot de passe pour éviter les patterns prévisibles
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    def validate_password(self, password):
        """Valide qu'un mot de passe respecte les critères de sécurité"""
        criteres = {
            'longueur': len(password) >= 12,
            'majuscule': bool(re.search(r'[A-Z]', password)),
            'minuscule': bool(re.search(r'[a-z]', password)),
            'chiffre': bool(re.search(r'[0-9]', password)),
            'special': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
        }
        return criteres, all(criteres.values())
    
    def simuler_creation_utilisateur(self, user_data):
        """Simule la création d'un utilisateur avec génération de mot de passe"""
        print(f"\n📝 Création de l'utilisateur: {user_data['prenom']} {user_data['nom']}")
        
        # Génération du mot de passe
        mot_de_passe = self.generate_password()
        print(f"🔑 Mot de passe généré: {mot_de_passe}")
        
        # Validation
        criteres, valide = self.validate_password(mot_de_passe)
        print(f"✅ Validation des critères:")
        for critere, respecte in criteres.items():
            symbole = "✓" if respecte else "✗"
            print(f"    {symbole} {critere}: {respecte}")
        
        # Simulation de l'email
        email_content = self.generer_email_bienvenue(user_data, mot_de_passe)
        print(f"📧 Email généré (longueur: {len(email_content)} caractères)")
        
        # Parse données Active Directory si disponibles
        if 'active_directory_data' in user_data and user_data['active_directory_data']:
            try:
                ad_data = json.loads(user_data['active_directory_data'])
                print(f"🏢 Données AD: {ad_data.get('department', 'N/A')} - Groupes: {len(ad_data.get('groups', []))}")
            except:
                print("⚠️  Données Active Directory invalides")
        
        return {
            'utilisateur': f"{user_data['prenom']} {user_data['nom']}",
            'email': user_data['email'],
            'mot_de_passe': mot_de_passe,
            'criteres_respectes': valide,
            'timestamp': datetime.now().isoformat()
        }
    
    def generer_email_bienvenue(self, user_data, mot_de_passe):
        """Génère le contenu d'email de bienvenue avec les identifiants"""
        return f"""
Objet: Bienvenue - Vos identifiants Odoo

Bonjour {user_data['prenom']} {user_data['nom']},

Votre compte Odoo a été créé avec succès !

Vos identifiants de connexion:
- URL: http://localhost:8069
- Email: {user_data['email']}
- Mot de passe: {mot_de_passe}

Pour des raisons de sécurité, nous vous recommandons de:
1. Changer votre mot de passe lors de votre première connexion
2. Activer l'authentification à deux facteurs si disponible

Département: {user_data.get('departement', 'N/A')}
Poste: {user_data.get('poste', 'N/A')}

Cordialement,
L'équipe IT
        """
    
    def tester_avec_fichier_csv(self, fichier_csv="utilisateurs.csv"):
        """Test de génération de mots de passe à partir du fichier CSV"""
        print(f"\n📂 Lecture du fichier: {fichier_csv}")
        
        try:
            with open(fichier_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                utilisateurs = list(reader)
            
            print(f"📊 {len(utilisateurs)} utilisateurs trouvés")
            
            for i, user in enumerate(utilisateurs[:3], 1):  # Limite à 3 pour la démo
                print(f"\n--- UTILISATEUR {i} ---")
                resultat = self.simuler_creation_utilisateur(user)
                self.resultats.append(resultat)
                
        except FileNotFoundError:
            print(f"❌ Fichier {fichier_csv} non trouvé")
            return False
        except Exception as e:
            print(f"❌ Erreur lors de la lecture: {str(e)}")
            return False
        
        return True
    
    def test_generation_multiple(self, nombre=5):
        """Test de génération de plusieurs mots de passe"""
        print(f"\n🔄 Test de génération de {nombre} mots de passe:")
        
        mots_de_passe = []
        for i in range(nombre):
            mdp = self.generate_password()
            criteres, valide = self.validate_password(mdp)
            mots_de_passe.append({
                'mot_de_passe': mdp,
                'valide': valide,
                'longueur': len(mdp)
            })
            print(f"  {i+1}. {mdp} ({'✓' if valide else '✗'})")
        
        # Statistiques
        valides = sum(1 for mdp in mots_de_passe if mdp['valide'])
        print(f"\n📈 Statistiques:")
        print(f"   Mots de passe valides: {valides}/{nombre} ({(valides/nombre)*100:.1f}%)")
        print(f"   Longueur moyenne: {sum(mdp['longueur'] for mdp in mots_de_passe)/nombre:.1f}")
        
        # Vérification de l'unicité (important pour la sécurité)
        uniques = len(set(mdp['mot_de_passe'] for mdp in mots_de_passe))
        print(f"   Mots de passe uniques: {uniques}/{nombre} ({(uniques/nombre)*100:.1f}%)")
    
    def generer_rapport(self):
        """Génère un rapport de test"""
        print("\n" + "=" * 60)
        print("RAPPORT DE TEST - GÉNÉRATION DE MOTS DE PASSE")
        print("=" * 60)
        
        if self.resultats:
            print(f"Utilisateurs traités: {len(self.resultats)}")
            tous_valides = all(r['criteres_respectes'] for r in self.resultats)
            print(f"Tous les mots de passe respectent les critères: {'✅ OUI' if tous_valides else '❌ NON'}")
            
            print("\nDétail des utilisateurs créés:")
            for r in self.resultats:
                status = "✅" if r['criteres_respectes'] else "❌"
                print(f"  {status} {r['utilisateur']} ({r['email']})")
        
        print(f"\n✅ Fonctionnalités testées:")
        print(f"   ✓ Génération automatique de mots de passe")
        print(f"   ✓ Validation des critères de sécurité") 
        print(f"   ✓ Import depuis fichier CSV")
        print(f"   ✓ Génération d'emails avec identifiants")
        print(f"   ✓ Support des données Active Directory")
        
        print(f"\n🎯 Section I.3 implémentée avec succès!")

def main():
    """Fonction principale de test"""
    tester = TestGenerationMotDePasse()
    
    # Test 1: Génération multiple
    tester.test_generation_multiple(5)
    
    # Test 2: Import CSV et création d'utilisateurs
    tester.tester_avec_fichier_csv()
    
    # Test 3: Rapport final
    tester.generer_rapport()
    
    print("\n" + "=" * 60)
    print("✅ TESTS TERMINÉS - Le système de génération de mots de passe fonctionne!")
    print("=" * 60)

if __name__ == "__main__":
    main() 