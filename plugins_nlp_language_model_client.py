import os
import requests
from typing import Dict, Any
from pydantic import BaseModel, Field
from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class LLMParams(BaseModel):
    prompt: str
    model: str = Field("gpt-4o-mini", description="Model to use for completion.")
    max_tokens: int = Field(150, gt=0)
    temperature: float = Field(0.7, ge=0.0, le=2.0)

class LLMResult(BaseModel):
    response_text: str
    model_used: str

class LanguageModelClientCapability(ExecutableCapability):
    """Interact with an OpenAI-compatible chat completions API."""

    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "nlp.language_model_client",
            "name": "External Language Model Client",
            "version": "1.0.0",
            "description": "Connects to an OpenAI-compatible API to generate text completions.",
            "dependencies": ["requests", "pydantic"],
            "input_schema": LLMParams.model_json_schema(),
            "output_schema": LLMResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = LLMParams(**params)
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set.")
        headers = {"Authorization": f"Bearer {api_key}"}
        json_data = {
            "model": p.model,
            "messages": [{"role": "user", "content": p.prompt}],
            "max_tokens": p.max_tokens,
            "temperature": p.temperature,
        }
        try:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers, json=json_data, timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            text = data["choices"][0]["message"]["content"]
            result = LLMResult(response_text=text, model_used=p.model)
            return result.model_dump()
        except requests.RequestException as e:
            raise RuntimeError(f"LLM API call failed: {e}")
