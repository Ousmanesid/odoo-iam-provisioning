# Système de Provisionnement IAM pour Odoo

## Vue d'ensemble

Ce projet implémente un système complet de provisionnement IAM (Identity and Access Management) pour Odoo, comprenant :

1. **Scripts Python** pour l'import et la gestion des utilisateurs
2. **API FastAPI** pour l'interface de provisionnement
3. **Application React** pour l'interface utilisateur web
4. **Integration avec Active Directory** via les structures JSON spécifiées

## Architecture du Projet

```
projet-odoo-iam/
├── odoo_user_provisioning.py    # Script d'import CSV (Partie I)
├── odoo_user_management.py      # Gestion des utilisateurs (Partie II) 
├── odoo_api.py                  # API FastAPI (Partie III)
├── requirements.txt             # Dépendances Python
├── utilisateurs.csv             # Fichier de données d'exemple
├── odoo-user-management/        # Application React
│   ├── src/
│   │   ├── components/
│   │   │   ├── CreateUser.tsx
│   │   │   ├── UpdateUser.tsx
│   │   │   ├── DeleteUser.tsx
│   │   │   ├── UserList.tsx
│   │   │   └── UserRoles.tsx
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── index.css
│   ├── public/
│   │   └── index.html
│   └── package.json
└── README_PROJET_COMPLET.md     # Ce fichier
```

## Partie I : Import automatique des utilisateurs

### Fonctionnalités
- ✅ Connexion à Odoo via API JSON-RPC
- ✅ Création d'utilisateurs depuis un fichier CSV
- ✅ Génération automatique de mots de passe sécurisés
- ✅ Attribution des droits/groupes
- ✅ Envoi d'emails avec les identifiants
- ✅ Système de logging complet

### Utilisation
```bash
python odoo_user_provisioning.py
```

### Structure du fichier CSV
```csv
nom,prenom,numero_utilisateur,login,email,adresse,droits
Dupont,Jean,1001,jean.dupont@iutcv.fr,jean.dupont@iutcv.fr,"123 Rue de la République",Administration
```

## Partie II : Gestion des comptes existants

### Fonctionnalités
- ✅ Recherche d'utilisateurs existants
- ✅ Modification des informations (email, mot de passe, etc.)
- ✅ Gestion des groupes/rôles (ajout/suppression)
- ✅ Suppression d'utilisateurs
- ✅ Logging de toutes les opérations

### Utilisation
```bash
python odoo_user_management.py
```

## Partie III : API de Provisionnement FastAPI

### Fonctionnalités
- ✅ API REST complète avec documentation automatique
- ✅ Support de la structure JSON Active Directory
- ✅ Endpoints pour toutes les opérations CRUD
- ✅ Gestion des rôles et permissions
- ✅ Validation des données avec Pydantic
- ✅ Support CORS pour React

### Endpoints disponibles

#### Utilisateurs
- `POST /users/` - Créer un utilisateur
- `GET /users/{user_id}` - Récupérer un utilisateur
- `PUT /users/{user_id}` - Modifier un utilisateur
- `DELETE /users/{user_id}` - Supprimer un utilisateur

#### Rôles
- `GET /users/{user_id}/roles` - Lister les rôles d'un utilisateur
- `POST /users/{user_id}/roles` - Attribuer des rôles
- `DELETE /users/{user_id}/roles` - Retirer des rôles

#### Groupes
- `GET /groups/` - Lister tous les groupes
- `GET /groups/search/{group_name}` - Rechercher un groupe

#### Utilitaires
- `GET /` - Statut de l'API
- `GET /health` - Vérification de santé

### Structure JSON Active Directory

```json
{
  "user_account": {
    "login_name": "john.doe@example.com",
    "other_ids": {
      "id": "CN=John Doe,OU=Users,DC=example,DC=com",
      "guid": "550e8400-e29b-41d4-a716-446655440000",
      "up_id": "123456",
      "display_name": "John Doe"
    }
  },
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "password123",
  "groups": [1, 2, 3]
}
```

### Démarrage de l'API
```bash
# Installation des dépendances
pip install -r requirements.txt

# Démarrage du serveur
python odoo_api.py
# ou
uvicorn odoo_api:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur : http://localhost:8000
Documentation interactive : http://localhost:8000/docs

## Partie IV : Interface React

### Fonctionnalités
- ✅ Interface moderne avec Bootstrap 5
- ✅ Formulaires pour toutes les opérations
- ✅ Gestion en temps réel des erreurs
- ✅ Support complet de la structure JSON AD
- ✅ Navigation par onglets
- ✅ Validation côté client

### Composants React
- **CreateUser** : Création d'utilisateurs avec métadonnées AD
- **UpdateUser** : Modification d'utilisateurs existants
- **DeleteUser** : Suppression sécurisée avec confirmation
- **UserList** : Liste et recherche d'utilisateurs
- **UserRoles** : Gestion des rôles et permissions

### Démarrage de l'application React
```bash
cd odoo-user-management

# Installation des dépendances (si npm est disponible)
npm install

# Démarrage en mode développement
npm start
```

L'application sera accessible sur : http://localhost:3000

## Installation et Configuration

### Prérequis
- Python 3.8+
- Odoo 15+ accessible
- Node.js 16+ (pour React)
- Serveur SMTP configuré (pour les emails)

### Configuration Odoo
Modifiez les variables de configuration dans chaque fichier :

```python
ODOO_URL = "http://localhost:8069"
ODOO_DB = "votre_base_odoo"
ODOO_USER = "admin"
ODOO_PASSWORD = "votre_mot_de_passe"
```

### Configuration Email
```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "votre-email@gmail.com"
SMTP_PASSWORD = "votre-mot-de-passe-app"
```

### Installation complète
```bash
# 1. Cloner le projet
git clone <url-du-projet>
cd projet-odoo-iam

# 2. Installer les dépendances Python
pip install -r requirements.txt

# 3. Configurer les paramètres Odoo dans les fichiers

# 4. Tester la connexion Odoo
python -c "import odoo_api; print('API OK')"

# 5. Démarrer l'API
uvicorn odoo_api:app --reload &

# 6. Démarrer l'application React (si Node.js est disponible)
cd odoo-user-management
npm install && npm start
```

## Tests et Validation

### Test de l'API avec curl

```bash
# Test de santé
curl -X GET "http://localhost:8000/health"

# Créer un utilisateur
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_account": {
      "login_name": "test@example.com",
      "other_ids": {
        "display_name": "Test User",
        "id": "CN=Test,OU=Users,DC=example,DC=com",
        "guid": "test-guid",
        "up_id": "12345"
      }
    },
    "name": "Test User",
    "email": "test@example.com",
    "groups": []
  }'

# Lister les groupes
curl -X GET "http://localhost:8000/groups/"
```

### Scripts de test
Chaque module inclut des fonctions de test intégrées :

```bash
python odoo_user_provisioning.py  # Test import CSV
python odoo_user_management.py    # Test gestion utilisateurs
```

## Logs et Monitoring

Tous les fichiers de log sont créés automatiquement :
- `odoo_provisioning.log` - Import CSV
- `odoo_user_management.log` - Gestion utilisateurs
- Logs FastAPI dans la console

## Fonctionnalités Avancées

### SCIM Compliance
Le projet inclut les bases pour implémenter SCIM (System for Cross-domain Identity Management) :
- Structure JSON standardisée
- Endpoints RESTful conformes
- Gestion des métadonnées

### Intégration Active Directory
- Support des Distinguished Names (DN)
- Gestion des GUIDs
- Mapping des User Principal IDs
- Métadonnées étendues

### Sécurité
- Génération de mots de passe sécurisés
- Validation des données d'entrée
- Logging de toutes les opérations
- Gestion des erreurs robuste

## Dépannage

### Problèmes courants

1. **Erreur de connexion Odoo**
   - Vérifiez l'URL et les identifiants
   - Assurez-vous qu'Odoo est démarré
   - Vérifiez les permissions de l'utilisateur admin

2. **Erreur d'installation React**
   - Vérifiez que Node.js est installé
   - Utilisez une version LTS de Node.js
   - Essayez `npm cache clean --force`

3. **Erreurs d'envoi d'email**
   - Configurez correctement les paramètres SMTP
   - Utilisez un mot de passe d'application pour Gmail
   - Vérifiez les pare-feu

### Modes de débogage

```python
# Activer les logs détaillés
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contribution

### Structure de développement
- Code Python : PEP 8
- Code React : ESLint + Prettier
- Documentation : Markdown
- Tests : pytest pour Python

### Roadmap
- [ ] Authentification JWT
- [ ] Interface d'administration avancée
- [ ] Support multi-tenant
- [ ] Intégration LDAP native
- [ ] API GraphQL
- [ ] Tests automatisés complets

## Support

Pour toute question ou problème :
1. Consultez les logs d'erreur
2. Vérifiez la configuration
3. Testez les endpoints individuellement
4. Consultez la documentation Odoo

---

**Auteur** : Système IAM Odoo  
**Version** : 1.0.0  
**Date** : 2025-05-28  

*Ce projet est conçu pour être une solution complète de provisionnement IAM pour Odoo, intégrant les meilleures pratiques de sécurité et d'utilisabilité.* 