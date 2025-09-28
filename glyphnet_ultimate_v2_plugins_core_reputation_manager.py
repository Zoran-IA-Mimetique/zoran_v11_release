from typing import Dict, Any, List, Literal, Optional, Tuple
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class ReputationState(BaseModel):
    scores: Dict[str, float] = {}

class ReputationManagerParams(BaseModel):
    action: Literal["update_score", "get_score", "leaderboard"]
    current_state: ReputationState
    entity_id: Optional[str] = None
    score_delta: Optional[float] = None

class ReputationManagerResult(BaseModel):
    action_performed: str
    updated_state: ReputationState
    result: Any

class ReputationManagerCapability(ExecutableCapability):
    """
    Gère un système de score de réputation pour des entités de manière stateless.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.stateless_reputation_manager",
            "name": "Stateless Reputation Manager",
            "version": "2.0.0",
            "description": "Manages entity reputation scores statelessly.",
            "dependencies": ["pydantic"],
            "input_schema": ReputationManagerParams.model_json_schema(),
            "output_schema": ReputationManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = ReputationManagerParams(**params)
        updated_state = p.current_state.copy(deep=True)
        action_result = None

        if p.action == "update_score":
            if p.entity_id is None or p.score_delta is None:
                raise ValueError("'entity_id' and 'score_delta' are required for 'update_score' action.")
            
            current_score = updated_state.scores.get(p.entity_id, 0.0)
            new_score = current_score + p.score_delta
            updated_state.scores[p.entity_id] = new_score
            action_result = {"entity_id": p.entity_id, "new_score": new_score}

        elif p.action == "get_score":
            if p.entity_id is None:
                raise ValueError("'entity_id' is required for 'get_score' action.")
            score = updated_state.scores.get(p.entity_id, 0.0)
            action_result = {"entity_id": p.entity_id, "score": score}

        elif p.action == "leaderboard":
            sorted_scores: List[Tuple[str, float]] = sorted(
                updated_state.scores.items(), key=lambda item: item[1], reverse=True
            )
            action_result = {"leaderboard": sorted_scores}

        result = ReputationManagerResult(
            action_performed=p.action,
            updated_state=updated_state,
            result=action_result
        )
        return result.model_dump()
