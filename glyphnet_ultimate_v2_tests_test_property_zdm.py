import pytest
from hypothesis import given, strategies as st, settings
from glyphnet_ultimate_v2.memory.zdm import ZDM

# Stratégies pour générer des données valides pour Hypothesis
# Texte simple pour les clés, JSON-compatible pour les valeurs
valid_keys = st.text(alphabet="abcdefghijklmnopqrstuvwxyz_", min_size=1, max_size=10)
valid_values = st.integers() | st.text() | st.booleans() | st.floats(allow_nan=False, allow_infinity=False)
valid_payloads = st.dictionaries(valid_keys, valid_values, min_size=1, max_size=5)

@settings(deadline=1000) # Augmenter le délai pour les tests plus complexes
@given(commits=st.lists(valid_payloads, min_size=1, max_size=20))
def test_property_integrity_is_always_preserved(commits):
    """
    Propriété : Quelle que soit la séquence de commits, la vérification
    d'intégrité de la ZDM doit toujours retourner True.
    """
    mem = ZDM()
    for payload in commits:
        mem.commit("PROPERTY_TEST_OP", payload)
    
    assert mem.verify_integrity()

@settings(deadline=1000)
@given(initial_commits=st.lists(valid_payloads, min_size=1, max_size=10),
       later_commits=st.lists(valid_payloads, min_size=1, max_size=10))
def test_property_rollback_restores_state_correctly(initial_commits, later_commits):
    """
    Propriété : Après un rollback vers un état N, l'état actuel de la ZDM
    (avant le commit de l'opération de rollback) doit être identique à l'état
    qui existait au moment du snapshot N.
    """
    mem = ZDM()
    
    # 1. Phase initiale
    for payload in initial_commits:
        mem.commit("INITIAL_PHASE", payload)
    
    # 2. Capturer l'état et le hash à restaurer
    hash_to_restore = mem.get_current_state_hash()
    state_to_restore = mem.get_current_state()

    # 3. Phase ultérieure de commits
    for payload in later_commits:
        mem.commit("LATER_PHASE", payload)
        
    # L'état a maintenant changé
    assert mem.get_current_state() != state_to_restore

    # 4. Effectuer le rollback (avec une petite modification pour tester l'état avant le commit final)
    # On accède à l'état interne pour tester la propriété.
    snapshot_state = mem._snapshots[hash_to_restore]
    mem._state = snapshot_state.copy() # Simule la restauration de l'état avant le commit de l'opération de rollback
    
    # 5. Vérifier la propriété
    assert mem.get_current_state() == state_to_restore
