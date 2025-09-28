import os
import json
from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class StorageManagerParams(BaseModel):
    action: Literal["save", "load", "delete"]
    base_path: str = Field("./glyphnet_storage", description="Base directory for storage operations.")
    object_name: str
    data_to_save: Optional[Dict[str, Any]] = None # for 'save'

class StorageManagerResult(BaseModel):
    action_performed: str
    status: str
    file_path: Optional[str] = None
    loaded_data: Optional[Dict[str, Any]] = None

class StorageManagerCapability(ExecutableCapability):
    """
    Gère le stockage et le chargement de documents JSON sur le système de fichiers.
    ATTENTION: Cette capacité interagit avec le système de fichiers et doit être
    exécutée dans un environnement hautement contrôlé.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.filesystem_storage_manager",
            "name": "Filesystem Storage Manager",
            "version": "2.0.0",
            "description": "Manages saving and loading JSON documents to the local filesystem.",
            "dependencies": ["pydantic"],
            "input_schema": StorageManagerParams.model_json_schema(),
            "output_schema": StorageManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = StorageManagerParams(**params)
        
        # Sécurisation du chemin pour éviter les traversées de répertoire
        if ".." in p.object_name or "/" in p.object_name:
            raise ValueError("Object name cannot contain path traversal characters.")
        
        os.makedirs(p.base_path, exist_ok=True)
        file_path = os.path.join(p.base_path, f"{p.object_name}.json")

        if p.action == "save":
            if p.data_to_save is None:
                raise ValueError("'data_to_save' is required for 'save' action.")
            try:
                with open(file_path, "w") as f:
                    json.dump(p.data_to_save, f, indent=2)
                return StorageManagerResult(action_performed="save", status="success", file_path=file_path).model_dump()
            except IOError as e:
                raise RuntimeError(f"Failed to save file: {e}")

        elif p.action == "load":
            if not os.path.exists(file_path):
                return StorageManagerResult(action_performed="load", status="not_found", file_path=file_path).model_dump()
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                return StorageManagerResult(action_performed="load", status="success", file_path=file_path, loaded_data=data).model_dump()
            except (IOError, json.JSONDecodeError) as e:
                raise RuntimeError(f"Failed to load or parse file: {e}")

        elif p.action == "delete":
            if os.path.exists(file_path):
                os.remove(file_path)
                return StorageManagerResult(action_performed="delete", status="success", file_path=file_path).model_dump()
            else:
                return StorageManagerResult(action_performed="delete", status="not_found", file_path=file_path).model_dump()
        
        raise ValueError(f"Unknown action: {p.action}")
