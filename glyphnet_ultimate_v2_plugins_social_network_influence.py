import networkx as nx
import random
from typing import Dict, Any, List
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class NetworkInfluenceParams(BaseModel):
    num_nodes: int = Field(20, gt=1)
    edge_probability: float = Field(0.1, ge=0, le=1)
    simulation_steps: int = Field(5, gt=0)
    infection_probability: float = Field(0.5, ge=0, le=1)

class NetworkInfluenceResult(BaseModel):
    simulation_history: List[Dict[int, int]]
    final_infected_count: int
    initial_spreader_node: int

class NetworkInfluenceCapability(ExecutableCapability):
    """
    Simule la diffusion d'une information (modèle SI - Susceptible-Infected)
    dans un réseau aléatoire.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "social.information_spread",
            "name": "Information Spread Simulation (SI Model)",
            "version": "2.0.0",
            "description": "Simulates the spread of information in a random network.",
            "dependencies": ["networkx", "pydantic"],
            "input_schema": NetworkInfluenceParams.model_json_schema(),
            "output_schema": NetworkInfluenceResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = NetworkInfluenceParams(**params)

        G = nx.erdos_renyi_graph(p.num_nodes, p.edge_probability)
        states = {node: 0 for node in G.nodes} # 0: Susceptible, 1: Infected
        
        if not G.nodes:
            return NetworkInfluenceResult(simulation_history=[], final_infected_count=0, initial_spreader_node=-1).model_dump()

        starter_node = random.choice(list(G.nodes))
        states[starter_node] = 1
        
        history = [states.copy()]

        for _ in range(p.simulation_steps):
            newly_infected = []
            # Parcourir les nœuds infectés pour voir s'ils infectent leurs voisins
            infected_nodes = [node for node, state in states.items() if state == 1]
            
            for node in infected_nodes:
                for neighbor in G.neighbors(node):
                    if states[neighbor] == 0 and random.random() < p.infection_probability:
                        newly_infected.append(neighbor)
            
            for node in newly_infected:
                states[node] = 1

            history.append(states.copy())

        result = NetworkInfluenceResult(
            simulation_history=history,
            final_infected_count=sum(states.values()),
            initial_spreader_node=starter_node
        )
        return result.model_dump()
