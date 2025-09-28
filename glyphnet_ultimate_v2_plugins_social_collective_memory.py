import random
from collections import deque
from typing import Dict, Any, List
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class CollectiveMemoryParams(BaseModel):
    num_agents: int = Field(10, gt=1)
    agent_memory_size: int = Field(5, gt=0)
    simulation_steps: int = Field(10, gt=0)
    num_event_types: int = Field(100, gt=0)
    sharing_probability: float = Field(0.5, ge=0, le=1)

class CollectiveMemoryResult(BaseModel):
    event_log: List[str]
    final_memories: Dict[int, List[str]]
    memory_overlap_score: float

class CollectiveMemoryCapability(ExecutableCapability):
    """
    Simule la formation d'une mémoire collective au sein d'un groupe d'agents.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "social.collective_memory",
            "name": "Collective Memory Simulation",
            "version": "2.0.0",
            "description": "Simulates the formation and sharing of memories among agents.",
            "dependencies": ["pydantic"],
            "input_schema": CollectiveMemoryParams.model_json_schema(),
            "output_schema": CollectiveMemoryResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = CollectiveMemoryParams(**params)

        memories = {i: deque(maxlen=p.agent_memory_size) for i in range(p.num_agents)}
        event_log = []

        for step in range(p.simulation_steps):
            event = f"event_{random.randint(1, p.num_event_types)}"
            event_log.append(event)
            
            # Un agent "observe" l'événement et initie le partage
            sharer = random.randrange(p.num_agents)
            
            for agent_id in range(p.num_agents):
                # L'initiateur se souvient toujours, les autres ont une probabilité de se souvenir
                if agent_id == sharer or random.random() < p.sharing_probability:
                    memories[agent_id].append(event)
        
        # Calculer le score de chevauchement de la mémoire
        all_final_memories = [item for mem in memories.values() for item in mem]
        if not all_final_memories:
            overlap_score = 0.0
        else:
            # Score = (Taille de l'union des mémoires) / (Somme des tailles des mémoires individuelles)
            # Un score élevé signifie beaucoup de redondance (forte mémoire collective)
            unique_memories = len(set(all_final_memories))
            overlap_score = 1.0 - (unique_memories / len(all_final_memories)) if all_final_memories else 0.0

        result = CollectiveMemoryResult(
            event_log=event_log,
            final_memories={k: list(v) for k, v in memories.items()},
            memory_overlap_score=overlap_score
        )
        return result.model_dump()
