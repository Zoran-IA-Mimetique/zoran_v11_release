import itertools
from typing import Dict, Any, List, Tuple
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class KemenyVoteParams(BaseModel):
    ballots: List[List[str]] = Field(description="A list of ranked-choice ballots.")
    max_options: int = Field(8, description="Maximum number of options to prevent factorial explosion.")

class KemenyVoteResult(BaseModel):
    optimal_ranking: Tuple[str, ...]
    kendall_tau_score: int

class KemenyVoteCapability(ExecutableCapability):
    """
    Implémente la méthode de Kemeny-Young pour trouver le classement qui minimise
    les désaccords avec les classements individuels.
    ATTENTION: La complexité est factorielle. Ne pas utiliser avec plus de 8-10 options.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "governance.kemeny_young_vote",
            "name": "Kemeny-Young Ranking Aggregation",
            "version": "1.0.0-alpha",
            "description": "Finds the optimal consensus ranking using the Kemeny-Young method. Computationally expensive.",
            "dependencies": ["pydantic"],
            "input_schema": KemenyVoteParams.model_json_schema(),
            "output_schema": KemenyVoteResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = KemenyVoteParams(**params)
        
        if not p.ballots:
            raise ValueError("Ballot list cannot be empty.")

        options = sorted(list(set(itertools.chain.from_iterable(p.ballots))))
        
        if len(options) > p.max_options:
            raise ValueError(f"Too many options ({len(options)}) for Kemeny-Young. Maximum is {p.max_options}.")

        best_ranking = None
        max_score = -1

        for perm in itertools.permutations(options):
            current_score = 0
            # Pour chaque paire d'options, compter combien de bulletins les classent dans le même ordre que la permutation candidate
            for (x, y) in itertools.combinations(perm, 2):
                pairwise_preference_count = 0
                for ballot in p.ballots:
                    try:
                        if ballot.index(x) < ballot.index(y):
                            pairwise_preference_count += 1
                    except ValueError:
                        continue # Option not in this ballot
                # Ajouter le nombre de votes pour (x > y) ou (y > x), le plus élevé des deux
                current_score += max(pairwise_preference_count, len(p.ballots) - pairwise_preference_count)
            
            if current_score > max_score:
                max_score = current_score
                best_ranking = perm
        
        result = KemenyVoteResult(optimal_ranking=best_ranking, kendall_tau_score=max_score)
        return result.model_dump()
