# Configuration pour le système de provisionnement Odoo
# Copier ce fichier vers config.py et adapter les valeurs

# Configuration Odoo
ODOO_CONFIG = {
    "url": "http://localhost:8069",
    "database": "odoo_db", 
    "username": "admin",
    "password": "admin"
}

# Configuration Email SMTP
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_user": "your-email@gmail.com", 
    "smtp_password": "your-app-password",
    "enabled": False  # Mettre à True pour activer l'envoi d'emails
}

# Configuration des logs
LOGGING_CONFIG = {
    "log_file": "odoo_provisioning.log",
    "log_level": "INFO"
}

# Groupes par défaut à créer dans Odoo si ils n'existent pas
DEFAULT_GROUPS = [
    {"name": "Administration", "category": "Administration"},
    {"name": "Ventes", "category": "Sales"}, 
    {"name": "Comptabilité", "category": "Accounting"},
    {"name": "Ressources Humaines", "category": "Human Resources"}
]
