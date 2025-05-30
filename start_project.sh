#!/bin/bash

echo "=========================================="
echo "Système de Provisionnement IAM pour Odoo"
echo "=========================================="
echo ""

# Fonction pour vérifier si une commande existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Vérifier Python
if ! command_exists python3; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✅ Python 3 détecté"

# Vérifier pip
if ! command_exists pip3; then
    echo "❌ pip3 n'est pas installé"
    exit 1
fi

echo "✅ pip3 détecté"

# Installer les dépendances Python
echo ""
echo "📦 Installation des dépendances Python..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de l'installation des dépendances"
    exit 1
fi

echo "✅ Dépendances Python installées"

# Menu principal
echo ""
echo "Que souhaitez-vous faire ?"
echo "1) Tester l'import CSV (Partie I)"
echo "2) Tester la gestion des utilisateurs (Partie II)"
echo "3) Démarrer l'API FastAPI (Partie III)"
echo "4) Démarrer l'application React (Partie IV)"
echo "5) Démarrer API + React"
echo "6) Tests complets"
echo "0) Quitter"
echo ""

read -p "Votre choix (0-6): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Lancement du test d'import CSV..."
        python3 odoo_user_provisioning.py
        ;;
    2)
        echo ""
        echo "🚀 Lancement du test de gestion des utilisateurs..."
        python3 odoo_user_management.py
        ;;
    3)
        echo ""
        echo "🚀 Démarrage de l'API FastAPI..."
        echo "L'API sera accessible sur: http://localhost:8000"
        echo "Documentation interactive: http://localhost:8000/docs"
        echo ""
        echo "Appuyez sur Ctrl+C pour arrêter"
        python3 odoo_api.py
        ;;
    4)
        echo ""
        if command_exists npm; then
            echo "🚀 Démarrage de l'application React..."
            cd odoo-user-management
            if [ ! -d "node_modules" ]; then
                echo "📦 Installation des dépendances React..."
                npm install
            fi
            echo "L'application sera accessible sur: http://localhost:3000"
            echo ""
            echo "Appuyez sur Ctrl+C pour arrêter"
            npm start
        else
            echo "❌ Node.js/npm n'est pas installé"
            echo "Pour installer Node.js :"
            echo "curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -"
            echo "sudo apt-get install -y nodejs"
        fi
        ;;
    5)
        echo ""
        echo "🚀 Démarrage de l'API et de React..."
        
        # Démarrer l'API en arrière-plan
        echo "Démarrage de l'API FastAPI..."
        python3 odoo_api.py &
        API_PID=$!
        
        # Attendre que l'API démarre
        sleep 3
        
        if command_exists npm; then
            echo "Démarrage de l'application React..."
            cd odoo-user-management
            if [ ! -d "node_modules" ]; then
                echo "📦 Installation des dépendances React..."
                npm install
            fi
            
            echo ""
            echo "✅ Services démarrés :"
            echo "   - API: http://localhost:8000"
            echo "   - React: http://localhost:3000"
            echo ""
            echo "Appuyez sur Ctrl+C pour arrêter les deux services"
            
            # Fonction de nettoyage
            cleanup() {
                echo ""
                echo "🛑 Arrêt des services..."
                kill $API_PID 2>/dev/null
                exit 0
            }
            
            trap cleanup SIGINT
            
            npm start
        else
            echo "❌ Node.js/npm n'est pas installé - démarrage API seulement"
            echo "API accessible sur: http://localhost:8000"
            wait $API_PID
        fi
        ;;
    6)
        echo ""
        echo "🧪 Exécution des tests complets..."
        echo ""
        
        # Test 1: Import CSV
        echo "Test 1: Import CSV"
        echo "=================="
        python3 -c "
from odoo_user_provisioning import OdooUserProvisioning
import sys

provisioning = OdooUserProvisioning()
uid = provisioning.authenticate()
if uid:
    print('✅ Connexion Odoo réussie')
    print('✅ Système de provisionnement opérationnel')
else:
    print('❌ Échec de connexion à Odoo')
    print('Vérifiez la configuration dans odoo_user_provisioning.py')
    sys.exit(1)
"
        
        echo ""
        
        # Test 2: Gestion utilisateurs
        echo "Test 2: Gestion des utilisateurs"
        echo "================================="
        python3 -c "
from odoo_user_management import OdooUserManagement
import sys

management = OdooUserManagement()
uid = management.authenticate()
if uid:
    print('✅ Module de gestion des utilisateurs opérationnel')
else:
    print('❌ Échec de connexion à Odoo pour la gestion')
    sys.exit(1)
"
        
        echo ""
        
        # Test 3: API
        echo "Test 3: API FastAPI"
        echo "==================="
        python3 -c "
import requests
import subprocess
import time
import signal
import os

# Démarrer l'API en arrière-plan
proc = subprocess.Popen(['python3', 'odoo_api.py'], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.DEVNULL)

# Attendre que l'API démarre
time.sleep(3)

try:
    # Test de l'endpoint de santé
    response = requests.get('http://localhost:8000/health', timeout=5)
    if response.status_code == 200:
        print('✅ API FastAPI opérationnelle')
        print('✅ Endpoint /health répond correctement')
    else:
        print('❌ L\'API ne répond pas correctement')
except requests.exceptions.RequestException:
    print('❌ Impossible de contacter l\'API')
    print('Vérifiez la configuration dans odoo_api.py')
finally:
    # Arrêter l'API
    proc.terminate()
    proc.wait()
"
        
        echo ""
        echo "🎉 Tests terminés !"
        echo ""
        echo "📁 Fichiers de logs créés :"
        echo "   - odoo_provisioning.log"
        echo "   - odoo_user_management.log"
        echo ""
        echo "📖 Consultez README_PROJET_COMPLET.md pour plus d'informations"
        ;;
    0)
        echo ""
        echo "👋 Au revoir !"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Choix invalide"
        exit 1
        ;;
esac 