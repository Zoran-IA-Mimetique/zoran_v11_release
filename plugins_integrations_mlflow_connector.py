from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel, Field
from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

try:
    import mlflow
    from mlflow.tracking import MlflowClient
    MLFLOW_AVAILABLE = True
except Exception:
    MLFLOW_AVAILABLE = False

class MLflowConnectorParams(BaseModel):
    action: Literal["log_model", "load_model"]
    run_id: str
    glyphnet_model: Optional[Dict[str, Any]] = None
    artifact_path: str = Field("governance", description="Path inside the run's artifacts.")

class MLflowConnectorResult(BaseModel):
    status: str
    glyphnet_model: Optional[Dict[str, Any]] = None

class MLflowConnectorCapability(ExecutableCapability):
    """Integrate GlyphNet with MLflow (log/load a governance model as an artifact)."""

    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "integrations.mlflow_connector",
            "name": "MLflow Connector",
            "version": "1.0.0",
            "description": "Logs or loads a GlyphNet model to/from an MLflow run's artifacts.",
            "dependencies": ["mlflow", "pydantic"],
            "input_schema": MLflowConnectorParams.model_json_schema(),
            "output_schema": MLflowConnectorResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        if not MLFLOW_AVAILABLE:
            raise RuntimeError("mlflow is not installed.")
        p = MLflowConnectorParams(**params)
        client = MlflowClient()

        if p.action == "log_model":
            if p.glyphnet_model is None:
                raise ValueError("glyphnet_model is required for action=log_model.")
            # Save as a JSON artifact
            tmp_path = "glyphnet_model.json"
            import json, tempfile, os
            with tempfile.TemporaryDirectory() as td:
                fp = os.path.join(td, tmp_path)
                with open(fp, "w", encoding="utf-8") as f:
                    json.dump(p.glyphnet_model, f, ensure_ascii=False, indent=2)
                artifact_uri = f"{p.artifact_path}/{tmp_path}"
                client.log_artifact(p.run_id, fp, artifact_path=p.artifact_path)
            return MLflowConnectorResult(status="logged").model_dump()

        elif p.action == "load_model":
            import tempfile, os, json
            with tempfile.TemporaryDirectory() as td:
                # Download the artifact directory first
                client.download_artifacts(p.run_id, p.artifact_path, td)
                fp = os.path.join(td, p.artifact_path, "glyphnet_model.json")
                with open(fp, "r", encoding="utf-8") as f:
                    model = json.load(f)
            return MLflowConnectorResult(status="loaded", glyphnet_model=model).model_dump()

        else:
            raise ValueError(f"Unsupported action: {p.action}")
