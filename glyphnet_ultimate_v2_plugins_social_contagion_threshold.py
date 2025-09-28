import random
import networkx as nx
from typing import Dict, Any, List
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class ContagionThresholdParams(BaseModel):
    num_agents: int = Field(20, gt=1)
    network_type: str = Field("erdos_renyi", description="Type of network topology to use.")
    connection_param: float = Field(0.2, description="Parameter for network creation (e.g., edge probability).")
    activation_threshold: int = Field(2, ge=1, description="Number of active neighbors required for an agent to become active.")
    simulation_steps: int = Field(10, gt=0)

class ContagionThresholdResult(BaseModel):
    simulation_history: List[Dict[int, int]]
    final_active_count: int

class ContagionThresholdCapability(ExecutableCapability):
    """
    Simule un modèle de contagion basé sur un seuil de voisins actifs (modèle de Granovetter).
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "social.threshold_contagion",
            "name": "Threshold Contagion Model",
            "version": "2.0.0",
            "description": "Simulates a contagion process based on an activation threshold.",
            "dependencies": ["networkx", "pydantic"],
            "input_schema": ContagionThresholdParams.model_json_schema(),
            "output_schema": ContagionThresholdResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = ContagionThresholdParams(**params)

        if p.network_type == "erdos_renyi":
            G = nx.erdos_renyi_graph(p.num_agents, p.connection_param)
        else:
            raise ValueError(f"Unsupported network type: {p.network_type}")

        states = {node: 0 for node in G.nodes} # 0: Inactive, 1: Active
        if not G.nodes:
            return ContagionThresholdResult(simulation_history=[], final_active_count=0).model_dump()

        # Initialiser avec un seul agent actif
        starter = random.choice(list(G.nodes))
        states[starter] = 1
        history = [states.copy()]

        for _ in range(p.simulation_steps):
            newly_activated = []
            inactive_nodes = [node for node, state in states.items() if state == 0]

            for node in inactive_nodes:
                neighbors = list(G.neighbors(node))
                active_neighbors = sum(states[neighbor] for neighbor in neighbors)
                if active_neighbors >= p.activation_threshold:
                    newly_activated.append(node)

            if not newly_activated: # La contagion s'arrête si personne de nouveau n'est activé
                break
            
            for node in newly_activated:
                states[node] = 1
            history.append(states.copy())

        result = ContagionThresholdResult(
            simulation_history=history,
            final_active_count=sum(states.values())
        )
        return result.model_dump()
