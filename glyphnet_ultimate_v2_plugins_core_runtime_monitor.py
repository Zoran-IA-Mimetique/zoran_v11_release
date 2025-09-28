from typing import Dict, Any
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

# Import optionnel, pour que le module puisse être importé même si psutil n'est pas là
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class RuntimeMonitorParams(BaseModel):
    pass # Pas de paramètres

class SystemMetrics(BaseModel):
    cpu_percent: float
    memory_percent: float
    disk_percent: float

class RuntimeMonitorCapability(ExecutableCapability):
    """
    Fournit des métriques système de base sur l'utilisation du CPU, de la mémoire et du disque.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.runtime_monitor",
            "name": "System Runtime Monitor",
            "version": "2.0.0",
            "description": "Provides basic system metrics (CPU, memory, disk).",
            "dependencies": ["psutil", "pydantic"],
            "input_schema": RuntimeMonitorParams.model_json_schema(),
            "output_schema": SystemMetrics.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        if not PSUTIL_AVAILABLE:
            raise RuntimeError("The 'psutil' library is not installed. Please run 'pip install psutil'.")
        
        # Validation vide, mais bonne pratique
        RuntimeMonitorParams(**params)
        
        metrics = SystemMetrics(
            cpu_percent=psutil.cpu_percent(interval=0.1),
            memory_percent=psutil.virtual_memory().percent,
            disk_percent=psutil.disk_usage("/").percent,
        )
        return metrics.model_dump()
