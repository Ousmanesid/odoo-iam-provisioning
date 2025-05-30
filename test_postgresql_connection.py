#!/usr/bin/env python3
"""
Script de test pour vérifier la connexion PostgreSQL avec Odoo
"""

import psycopg2
import sys

def test_postgresql_connection():
    """Test de connexion à PostgreSQL"""
    try:
        # Paramètres de connexion
        connection_params = {
            'host': 'localhost',
            'database': 'odoo_iam_db',
            'user': 'odoo',
            'port': 5432
        }
        
        print("=== Test de connexion PostgreSQL ===")
        print(f"Connexion à: {connection_params}")
        
        # Tentative de connexion
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        
        print("✅ Connexion PostgreSQL réussie!")
        
        # Test de base: version PostgreSQL
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"Version PostgreSQL: {version}")
        
        # Lister les tables existantes
        cursor.execute("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public' 
            ORDER BY tablename;
        """)
        tables = cursor.fetchall()
        
        print(f"\nNombre de tables dans la base: {len(tables)}")
        if tables:
            print("Tables Odoo détectées:")
            for table in tables[:10]:  # Afficher les 10 premières
                print(f"  - {table[0]}")
            if len(tables) > 10:
                print(f"  ... et {len(tables) - 10} autres tables")
        else:
            print("Aucune table trouvée (base de données vide)")
        
        # Fermeture
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion PostgreSQL: {e}")
        return False

def test_odoo_tables():
    """Vérifier les tables spécifiques à Odoo"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='odoo_iam_db',
            user='odoo'
        )
        cursor = conn.cursor()
        
        # Tables importantes d'Odoo
        odoo_core_tables = [
            'ir_module_module',
            'res_users',
            'res_partner',
            'ir_model',
            'ir_config_parameter'
        ]
        
        print("\n=== Vérification des tables Odoo ===")
        for table in odoo_core_tables:
            cursor.execute(f"""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_name = '{table}' AND table_schema = 'public';
            """)
            exists = cursor.fetchone()[0] > 0
            status = "✅" if exists else "❌"
            print(f"{status} Table {table}: {'Existe' if exists else 'Manquante'}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Erreur lors de la vérification des tables: {e}")

if __name__ == "__main__":
    print("Test de la configuration PostgreSQL pour Odoo")
    print("=" * 50)
    
    success = test_postgresql_connection()
    if success:
        test_odoo_tables()
    else:
        sys.exit(1)
