from typing import Dict, Any, List, Literal
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class PipelineNodesParams(BaseModel):
    action: Literal["validate", "execute"]
    pipeline_nodes: conlist(str, min_length=1)
    # Paramètres d'action
    required_nodes: Optional[List[str]] = None # Pour 'validate'
    initial_context: Dict[str, Any] = {} # Pour 'execute'

class ValidationResult(BaseModel):
    is_valid: bool
    missing_nodes: List[str]

class ExecutionLogEntry(BaseModel):
    step_name: str
    status: str
    timestamp_utc: str

class ExecutionResult(BaseModel):
    execution_log: List[ExecutionLogEntry]
    final_context: Dict[str, Any]

class PipelineNodesResult(BaseModel):
    action_performed: str
    result: Any # ValidationResult or ExecutionResult

class PipelineNodesCapability(ExecutableCapability):
    """
    Capacité pour valider et simuler l'exécution de pipelines de nœuds logiques.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.logical_pipeline_manager",
            "name": "Logical Pipeline Manager",
            "version": "2.0.0",
            "description": "Validates and simulates the execution of logical pipeline nodes.",
            "dependencies": ["pydantic"],
            "input_schema": PipelineNodesParams.model_json_schema(),
            "output_schema": PipelineNodesResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = PipelineNodesParams(**params)
        
        if p.action == "validate":
            required = set(p.required_nodes) if p.required_nodes is not None else set()
            provided = set(p.pipeline_nodes)
            missing = sorted(list(required - provided))
            action_result = ValidationResult(is_valid=len(missing) == 0, missing_nodes=missing)

        elif p.action == "execute":
            import datetime
            context = p.initial_context.copy()
            log: List[ExecutionLogEntry] = []
            
            for node_name in p.pipeline_nodes:
                # Simulation d'exécution: la logique de chaque nœud serait dans un autre plugin.
                # Ici, on logue simplement l'exécution.
                log.append(ExecutionLogEntry(
                    step_name=node_name,
                    status="executed_successfully",
                    timestamp_utc=datetime.datetime.utcnow().isoformat() + "Z"
                ))
            
            action_result = ExecutionResult(execution_log=log, final_context=context)

        else:
            raise ValueError(f"Unknown action: {p.action}")

        result = PipelineNodesResult(action_performed=p.action, result=action_result)
        return result.model_dump()
