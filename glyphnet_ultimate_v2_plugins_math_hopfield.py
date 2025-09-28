import numpy as np
from typing import Dict, Any, List
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class HopfieldParams(BaseModel):
    patterns_to_store: List[conlist(int, min_length=1)] = Field(description="List of bipolar patterns (-1, 1) to store in the network.")
    initial_state: conlist(int, min_length=1) = Field(description="A (potentially corrupted) pattern to recall.")
    max_steps: int = Field(5, gt=0, le=100)

class HopfieldResult(BaseModel):
    recall_history: List[List[int]]
    final_recalled_state: List[int]
    is_stable: bool

class HopfieldCapability(ExecutableCapability):
    """
    Capacité simulant une mémoire associative simple avec un réseau de Hopfield.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "math.hopfield_network",
            "name": "Hopfield Associative Memory",
            "version": "2.0.0",
            "description": "Simulates training and recalling patterns in a Hopfield network.",
            "dependencies": ["numpy", "pydantic"],
            "input_schema": HopfieldParams.model_json_schema(),
            "output_schema": HopfieldResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = HopfieldParams(**params)
        patterns = np.array(p.patterns_to_store)
        num_patterns, size = patterns.shape

        if len(p.initial_state) != size:
            raise ValueError("Initial state must have the same dimension as the stored patterns.")

        # Entraînement (Règle de Hebb)
        W = np.dot(patterns.T, patterns) / num_patterns
        np.fill_diagonal(W, 0)

        # Rappel (Mise à jour asynchrone)
        state = np.array(p.initial_state)
        history = [state.tolist()]

        for _ in range(p.max_steps):
            prev_state = state.copy()
            # Mise à jour asynchrone : met à jour chaque neurone un par un dans un ordre aléatoire
            for i in np.random.permutation(size):
                state[i] = 1 if np.dot(W[i], state) >= 0 else -1
            history.append(state.tolist())
            if np.array_equal(state, prev_state):
                break # Le réseau a convergé vers un état stable

        result = HopfieldResult(
            recall_history=history,
            final_recalled_state=state.tolist(),
            is_stable=np.array_equal(history[-1], history[-2]) if len(history) > 1 else True
        )
        return result.model_dump()
