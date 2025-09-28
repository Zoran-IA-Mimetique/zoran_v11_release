import collections
from typing import Dict, Any, List, Tuple
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class BordaVoteParams(BaseModel):
    ballots: List[conlist(str, min_length=1, unique_items=True)] = Field(
        description="A list of ballots, where each ballot is a list of options ordered by preference."
    )

class BordaVoteResult(BaseModel):
    scores: Dict[str, int]
    ranking: List[Tuple[str, int]]
    winner: str

class BordaVoteCapability(ExecutableCapability):
    """
    Implémente la méthode de vote par décompte de Borda pour agréger les préférences.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "governance.borda_count_vote",
            "name": "Borda Count Voting",
            "version": "2.0.0",
            "description": "Aggregates ranked preferences using the Borda count method.",
            "dependencies": ["pydantic"],
            "input_schema": BordaVoteParams.model_json_schema(),
            "output_schema": BordaVoteResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = BordaVoteParams(**params)
        
        if not p.ballots:
            raise ValueError("Ballot list cannot be empty.")
            
        scores = collections.defaultdict(int)
        num_options = len(p.ballots[0])

        for ballot in p.ballots:
            if len(ballot) != num_options:
                raise ValueError("All ballots must have the same number of options.")
            for i, option in enumerate(ballot):
                # Le premier choix reçoit (n-1) points, le deuxième (n-2), etc.
                scores[option] += num_options - 1 - i
        
        ranking = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        winner = ranking[0][0] if ranking else None

        result = BordaVoteResult(
            scores=dict(scores),
            ranking=ranking,
            winner=winner
        )
        return result.model_dump()
