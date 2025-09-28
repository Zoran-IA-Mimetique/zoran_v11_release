import os
import psycopg2
from psycopg2.extras import Json

DATABASE_ZDM_URL = os.environ.get("GLYPHNET_ZDM_DATABASE_URL", "postgresql://user:password@localhost/zdm_db")

def get_zdm_db_connection():
    return psycopg2.connect(DATABASE_ZDM_URL)

def init_zdm_db():
    conn = get_zdm_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS zdm_logs (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL,
                operation VARCHAR(255) NOT NULL,
                payload JSONB NOT NULL,
                metadata JSONB,
                entry_hash VARCHAR(64) NOT NULL UNIQUE
            );
        """)
