from typing import Dict, Any, Tuple
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class ResourceManagerParams(BaseModel):
    pass # No parameters for this capability

class MemoryUsage(BaseModel):
    total: int
    available: int
    percent: float
    used: int
    free: int

class DiskUsage(BaseModel):
    total: int
    used: int
    free: int
    percent: float

class ResourceManagerResult(BaseModel):
    cpu_percent: float
    memory: MemoryUsage
    disk: DiskUsage

class ResourceManagerCapability(ExecutableCapability):
    """
    Fournit un aperçu des ressources système (CPU, Mémoire, Disque).
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.system_resource_monitor",
            "name": "System Resource Monitor",
            "version": "2.1.0",
            "description": "Provides a snapshot of system resource usage.",
            "dependencies": ["psutil", "pydantic"],
            "input_schema": ResourceManagerParams.model_json_schema(),
            "output_schema": ResourceManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        if not PSUTIL_AVAILABLE:
            raise RuntimeError("The 'psutil' library is not installed. Please run 'pip install psutil'.")

        ResourceManagerParams(**params)
        
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        
        result = ResourceManagerResult(
            cpu_percent=psutil.cpu_percent(interval=0.1),
            memory=MemoryUsage(**mem._asdict()),
            disk=DiskUsage(**disk._asdict())
        )
        return result.model_dump()
