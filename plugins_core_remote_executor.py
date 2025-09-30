# Capability Remote Executor
import requests
from typing import Dict, Any

class RemoteExecutor:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token

    def execute(self, capability_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.base_url}/capabilities/{capability_id}", json=params, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f"Remote execution failed: {response.text}")
        return response.json()
