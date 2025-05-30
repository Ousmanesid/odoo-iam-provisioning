# 🚀 Système de Provisionnement IAM pour Odoo

Un système complet de gestion des identités et des accès (IAM) pour Odoo, comprenant l'import automatique d'utilisateurs, une API REST et une interface web moderne.

## ✨ Fonctionnalités

### 🔄 Import Automatique d'Utilisateurs
- Import depuis fichiers CSV
- Génération automatique de mots de passe sécurisés
- Attribution des droits et groupes via API Odoo
- Envoi d'emails avec identifiants
- Système de logging complet

### 🔧 Gestion des Comptes
- Recherche d'utilisateurs par ID
- Modification des informations (email, mot de passe, etc.)
- Gestion des groupes et rôles (ajout/suppression)
- Suppression sécurisée avec confirmation

### 🌐 API REST & Interface Web
- API FastAPI complète avec endpoints CRUD
- Support structure JSON Active Directory (CN, GUID, User Principal ID)
- Interface React moderne avec Bootstrap 5
- Formulaires pour toutes les opérations
- Validation temps réel et gestion d'erreurs

## 🏗️ Architecture

```
odoo-iam-project/
├── 📁 Backend Python
│   ├── odoo_api.py              # API FastAPI complète
│   ├── odoo_user_management.py  # Gestion utilisateurs existants
│   ├── odoo_user_provisioning.py# Import automatique CSV
│   ├── config_template.py       # Configuration Odoo
│   └── requirements.txt         # Dépendances Python
│
├── 📁 Frontend React
│   └── odoo-user-management/    # Application React complète
│       ├── src/components/      # Composants React
│       ├── public/              # Assets publics
│       └── package.json         # Dépendances Node.js
│
├── 📁 Tests & Outils
│   ├── test_*.py               # Tests unitaires
│   ├── check_system_integrity.py
│   └── demo_iam_system.py
│
└── 📁 Documentation
    ├── README_PROJET_COMPLET.md
    ├── GUIDE_GITHUB.md
    └── RESULTATS_TESTS.md
```

## 🚀 Installation Rapide

### 1. Cloner le projet
```bash
git clone https://github.com/Ousmanesid/odoo-iam-provisioning.git
cd odoo-iam-provisioning
```

### 2. Configuration Backend
```bash
# Installer les dépendances Python
pip install -r requirements.txt

# Configurer Odoo
cp config_template.py config.py
# Éditer config.py avec vos paramètres Odoo
```

### 3. Lancer l'API
```bash
python odoo_api.py
# API disponible sur http://localhost:8000
```

### 4. Configuration Frontend
```bash
cd odoo-user-management
npm install
npm start
# Interface web sur http://localhost:3000
```

## 🔧 Configuration

### Paramètres Odoo (config.py)
```python
ODOO_CONFIG = {
    'url': 'http://localhost:8069',
    'db': 'votre_db',
    'username': 'admin',
    'password': 'votre_mot_de_passe'
}
```

### Structure CSV d'import
```csv
nom,prenom,email,login,groupe
Doe,John,john.doe@example.com,jdoe,user
Smith,Jane,jane.smith@example.com,jsmith,manager
```

## 📚 Utilisation

### Import d'utilisateurs
```python
from odoo_user_provisioning import import_users_from_csv
import_users_from_csv('utilisateurs.csv')
```

### API REST
```bash
# Créer un utilisateur
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "login": "jdoe", "email": "john@example.com"}'

# Lister les utilisateurs
curl "http://localhost:8000/users"
```

### Interface Web
1. Accéder à http://localhost:3000
2. Utiliser les formulaires pour gérer les utilisateurs
3. Consulter les logs en temps réel

## 🧪 Tests

```bash
# Tests des fonctionnalités principales
python test_odoo_connection.py
python test_generation_mot_de_passe.py
python test_odoo_complete_setup.py

# Vérification de l'intégrité système
python check_system_integrity.py
```

## 📖 Documentation Complète

- [Guide Complet](README_PROJET_COMPLET.md) - Documentation détaillée
- [Guide GitHub](GUIDE_GITHUB.md) - Déploiement et contribution
- [Résultats Tests](RESULTATS_TESTS.md) - Rapports de tests

## 🔐 Sécurité

- Génération de mots de passe sécurisés (majuscules, minuscules, chiffres, caractères spéciaux)
- Validation des données d'entrée avec Pydantic
- Logging de toutes les opérations sensibles
- Support HTTPS pour l'API en production

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit (`git commit -m 'Ajouter nouvelle fonctionnalité'`)
4. Push (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrir une Pull Request

## 📄 License

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 📞 Support

- Issues GitHub : [Signaler un problème](https://github.com/Ousmanesid/odoo-iam-provisioning/issues)
- Documentation : Consulter les fichiers MD du projet

---

⭐ **Si ce projet vous aide, n'hésitez pas à mettre une étoile !**
