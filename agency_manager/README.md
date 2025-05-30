# 🏢 Module Agency Manager - UberCircuit

## 📋 Description

Le module **Agency Manager** est un module Odoo dédié à la gestion des agences UberCircuit. Il permet de gérer des entreprises individuelles d'accompagnateurs avec leurs circuits et leurs équipes.

## ✨ Fonctionnalités

### 🏢 Gestion des Agences
- **Informations de base** : nom, SIRET, date de création, capital
- **Propriétaire** : prénom, nom, date et lieu de naissance
- **Contraintes** : SIRET unique
- **Statistiques** : nombre d'accompagnateurs et circuits

### 👥 Gestion des Accompagnateurs
- **Extension des partenaires Odoo** pour les accompagnateurs
- **Compétences** et tarifs horaires
- **Disponibilités** avec dates de début et fin
- **Relations** avec les agences partenaires

### 🗺️ Gestion des Circuits
- **Informations** : identifiant, nom, dates, prix
- **Assignment** d'accompagnateurs aux circuits
- **Description** détaillée et nombre maximum de participants
- **Validation** des dates (fin ≥ début)

## 🏗️ Structure Technique

```
agency_manager/
├── __manifest__.py          # Configuration du module
├── __init__.py              # Import des models
├── models/
│   ├── __init__.py          # Import du modèle agency
│   └── agency.py            # Modèles principaux
├── views/
│   └── agency_view.xml      # Vues et menus
└── security/
    └── ir.model.access.csv  # Droits d'accès
```

## 📊 Modèles de Données

### AgencyManager (`agency.manager`)
- Informations de l'agence et du propriétaire
- Relations Many2many avec les accompagnateurs
- Relations One2many avec les circuits
- Méthodes d'action pour les boutons intelligents

### ResPartner (extension de `res.partner`)
- Extension pour les accompagnateurs
- Champs spécialisés : compétences, tarifs, disponibilités
- Relations avec les agences

### AgencyCircuit (`agency.circuit`)
- Gestion des circuits touristiques
- Relations avec agences et accompagnateurs
- Contraintes de validation

## 🎯 Interface Utilisateur

### Menus
- **Agences UberCircuit** → **Gestion des Agences**
  - Agences Entreprises Individuelles
  - Circuits
  - Accompagnateurs

### Vues
- **Formulaires** avec onglets pour accompagnateurs et circuits
- **Listes** avec colonnes pertinentes
- **Boutons intelligents** pour les statistiques
- **Extension** du formulaire partenaire pour les accompagnateurs

## 🔧 Installation

1. **Copier** le module dans `/opt/odoo/addons/`
2. **Redémarrer** le service Odoo
3. **Activer** le mode développeur
4. **Mettre à jour** la liste des modules
5. **Installer** le module "Agency Manager"

## 📝 Contraintes de Validation

- **SIRET unique** par agence
- **Identifiant de circuit unique**
- **Dates cohérentes** pour les circuits (fin ≥ début)

## 🚀 Utilisation

1. **Créer des agences** avec leurs informations légales
2. **Ajouter des accompagnateurs** comme partenaires
3. **Définir les circuits** avec dates et prix
4. **Assigner** les accompagnateurs aux circuits
5. **Gérer** les relations agences-accompagnateurs

## 🎨 Fonctionnalités Avancées

- **Boutons intelligents** pour navigation rapide
- **Domaines** pour filtrer les accompagnateurs
- **Calculs automatiques** des compteurs
- **Validation** en temps réel des données

## 👨‍💻 Auteurs

- **Taiishiro**
- **Ousmanesid**

## 📄 Version

**1.0** - Version initiale avec toutes les fonctionnalités de base

---

*Module développé pour la gestion complète des agences de voyage UberCircuit* 🌍 