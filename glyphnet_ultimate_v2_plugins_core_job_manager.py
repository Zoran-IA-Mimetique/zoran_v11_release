import uuid
import time
from typing import Dict, Any, Literal, Optional, List
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class Job(BaseModel):
    task_name: str
    params: Dict[str, Any]
    status: Literal["pending", "running", "completed", "failed"]
    created_at: float
    updated_at: float

class JobState(BaseModel):
    jobs: Dict[str, Job] = {}

class JobManagerParams(BaseModel):
    action: Literal["create", "update", "get"]
    current_state: JobState
    task_name: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    job_id: Optional[str] = None
    status: Optional[Literal["pending", "running", "completed", "failed"]] = None

class JobManagerResult(BaseModel):
    action_performed: str
    updated_state: JobState
    result: Any

class JobManagerCapability(ExecutableCapability):
    """
    Gère un registre de jobs (tâches asynchrones) de manière stateless.
    L'état des jobs est géré par l'appelant.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.stateless_job_manager",
            "name": "Stateless Job Manager",
            "version": "2.0.0",
            "description": "Manages asynchronous jobs statelessly.",
            "dependencies": ["pydantic"],
            "input_schema": JobManagerParams.model_json_schema(),
            "output_schema": JobManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = JobManagerParams(**params)
        updated_state = p.current_state.copy(deep=True)
        action_result = None
        now = time.time()

        if p.action == "create":
            if not p.task_name:
                raise ValueError("'task_name' is required for 'create' action.")
            job_id = f"job_{uuid.uuid4().hex}"
            new_job = Job(
                task_name=p.task_name,
                params=p.params or {},
                status="pending",
                created_at=now,
                updated_at=now
            )
            updated_state.jobs[job_id] = new_job
            action_result = {"job_id": job_id, "status": "pending"}

        elif p.action == "update":
            if not p.job_id or not p.status:
                raise ValueError("'job_id' and 'status' are required for 'update' action.")
            if p.job_id in updated_state.jobs:
                updated_state.jobs[p.job_id].status = p.status
                updated_state.jobs[p.job_id].updated_at = now
                action_result = {"job_id": p.job_id, "status": p.status}
            else:
                action_result = {"error": "job_not_found"}

        elif p.action == "get":
            if not p.job_id:
                raise ValueError("'job_id' is required for 'get' action.")
            action_result = updated_state.jobs.get(p.job_id)
        
        result = JobManagerResult(action_performed=p.action, updated_state=updated_state, result=action_result)
        return result.model_dump()
