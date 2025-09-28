import os
import json
import pytest

try:
    from glyphnet_ultimate_v2.memory.zdm_pg import ZDM_PG, init_zdm_db, get_zdm_db_connection
except Exception:
    pytest.skip("glyphnet_ultimate_v2 not importable in flat batch layout; tests skipped.", allow_module_level=True)

@pytest.fixture(scope="module")
def persistent_zdm():
    conn = get_zdm_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS zdm_logs;")
    conn.commit()
    conn.close()
    init_zdm_db()
    zdm = ZDM_PG()
    yield zdm
    zdm.close()

@pytest.mark.skipif("GLYPHNET_ZDM_DATABASE_URL" not in os.environ, reason="Requires GLYPHNET_ZDM_DATABASE_URL for a test PostgreSQL DB.")
def test_zdm_commit_is_persistent(persistent_zdm):
    payload = {"data": "event_1"}
    persistent_zdm.commit("CREATE", payload)
    conn = get_zdm_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM zdm_logs;")
            count = cursor.fetchone()[0]
        assert count >= 1
    finally:
        conn.close()

@pytest.mark.skipif("GLYPHNET_ZDM_DATABASE_URL" not in os.environ, reason="Requires GLYPHNET_ZDM_DATABASE_URL for a test PostgreSQL DB.")
def test_zdm_state_reconstruction_from_db(persistent_zdm):
    persistent_zdm.commit("CREATE", {"id": "A", "value": 10})
    persistent_zdm.commit("UPDATE", {"id": "A", "value": 20})
    persistent_zdm.commit("CREATE", {"id": "B", "value": 5})
    reconstructed_state = persistent_zdm.get_current_state()
    assert reconstructed_state.get("id") == "B"
    assert reconstructed_state.get("value") == 5
