import os
import pytest
from glyphnet_ultimate_v2.memory.zdm_pg import ZDM_PG, init_zdm_db, get_zdm_db_connection

# These tests require a PostgreSQL URL in the environment:
# export GLYPHNET_ZDM_DATABASE_URL="postgresql://user:password@localhost/zdm_db"

@pytest.fixture(scope="module")
def persistent_zdm():
    """Initialize a persistent ZDM (PostgreSQL) for tests, then clean up."""
    conn = get_zdm_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS zdm_logs;")
    conn.commit()
    conn.close()

    init_zdm_db()
    zdm = ZDM_PG()
    try:
        yield zdm
    finally:
        zdm.close()

requires_db = pytest.mark.skipif(
    "GLYPHNET_ZDM_DATABASE_URL" not in os.environ,
    reason="Requires a test PostgreSQL database (GLYPHNET_ZDM_DATABASE_URL)."
)

@requires_db
def test_zdm_commit_is_persistent(persistent_zdm):
    """Verify that commits are written to the database."""
    payload = {"id": "A", "value": 10}
    persistent_zdm.commit("CREATE", payload)

    conn = get_zdm_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM zdm_logs;")
            count = cursor.fetchone()[0]
    finally:
        conn.close()

    assert count >= 1, "Commit was not inserted into the database."

@requires_db
def test_zdm_state_reconstruction_from_db(persistent_zdm):
    """State can be reconstructed from persistent log."""
    persistent_zdm.commit("CREATE", {"id": "A", "value": 10})
    persistent_zdm.commit("UPDATE", {"id": "A", "value": 20})
    persistent_zdm.commit("CREATE", {"id": "B", "value": 5})

    state = persistent_zdm.get_current_state()
    # Our simple reconstruction merges dicts in sequence; last keys win.
    assert isinstance(state, dict)
    assert state.get("id") in {"A", "B"}
