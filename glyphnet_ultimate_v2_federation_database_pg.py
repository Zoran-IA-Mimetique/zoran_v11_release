import os
import psycopg2
from psycopg2.extras import DictCursor

# Les paramètres de connexion sont chargés depuis l'environnement
DATABASE_URL = os.environ.get("GLYPHNET_DATABASE_URL", "postgresql://user:password@localhost/glyphnet_db")

def get_pg_connection():
    """Fournit une connexion à la base de données PostgreSQL."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_pg_db():
    """Initialise le schéma de la base de données PostgreSQL si nécessaire."""
    conn = get_pg_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proposals (
                id TEXT PRIMARY KEY,
                proposer_id TEXT NOT NULL,
                claim TEXT NOT NULL,
                details_json TEXT NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                proposal_id TEXT NOT NULL,
                voter_id TEXT NOT NULL,
                decision BOOLEAN NOT NULL,
                PRIMARY KEY (proposal_id, voter_id)
            );
        """)
    conn.commit()
    conn.close()
# Remplacer les imports et la dépendance
# from . import database -> from . import database_pg
# import sqlite3 -> import psycopg2
# def get_db_connection() -> def get_pg_connection()
# db: sqlite3.Connection -> db: psycopg2.extensions.connection

@app.post("/proposals")
async def submit_proposal(proposal: Proposal, db: psycopg2.extensions.connection = Depends(get_pg_connection)):
    proposal_id = f"prop_{uuid.uuid4().hex}"
    with db.cursor() as cursor:
        cursor.execute(
            "INSERT INTO proposals (id, proposer_id, claim, details_json) VALUES (%s, %s, %s, %s)",
            (proposal_id, proposal.proposer_id, proposal.claim, json.dumps(proposal.details))
        )
    db.commit()
    db.close()
    return {"proposal_id": proposal_id, "message": "Proposal submitted successfully."}
