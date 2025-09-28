import time
from typing import Dict, Any, List, Literal, Optional
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class MetricPoint(BaseModel):
    timestamp: float
    value: float

class MetricState(BaseModel):
    metrics: Dict[str, List[MetricPoint]] = {}

class MetricsManagerParams(BaseModel):
    action: Literal["record", "query"]
    current_state: MetricState
    metric_name: str
    value: Optional[float] = None # For 'record'
    query_method: Literal["average", "latest", "all"] = "average" # For 'query'

class MetricsManagerResult(BaseModel):
    action_performed: str
    updated_state: MetricState
    result: Any

class MetricsManagerCapability(ExecutableCapability):
    """
    Gère l'enregistrement et l'interrogation de métriques temporelles de manière stateless.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.stateless_metrics_manager",
            "name": "Stateless Metrics Manager",
            "version": "2.0.0",
            "description": "Manages recording and querying of time-series metrics statelessly.",
            "dependencies": ["pydantic"],
            "input_schema": MetricsManagerParams.model_json_schema(),
            "output_schema": MetricsManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = MetricsManagerParams(**params)
        updated_state = p.current_state.copy(deep=True)
        action_result = None
        
        if p.action == "record":
            if p.value is None:
                raise ValueError("'value' is required for 'record' action.")
            
            new_point = MetricPoint(timestamp=time.time(), value=p.value)
            if p.metric_name not in updated_state.metrics:
                updated_state.metrics[p.metric_name] = []
            updated_state.metrics[p.metric_name].append(new_point)
            action_result = new_point

        elif p.action == "query":
            metric_series = updated_state.metrics.get(p.metric_name, [])
            if not metric_series:
                action_result = None
            elif p.query_method == "average":
                values = [m.value for m in metric_series]
                action_result = sum(values) / len(values)
            elif p.query_method == "latest":
                action_result = metric_series[-1]
            elif p.query_method == "all":
                action_result = metric_series

        result = MetricsManagerResult(
            action_performed=p.action,
            updated_state=updated_state,
            result=action_result
        )
        return result.model_dump()
