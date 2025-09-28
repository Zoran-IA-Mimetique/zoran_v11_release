import numpy as np
from scipy.fft import fft, fftfreq
from typing import Dict, Any, List
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class SignalProcessingParams(BaseModel):
    signal: conlist(float, min_length=2)
    sample_rate: float = Field(1.0, gt=0)

class SignalProcessingResult(BaseModel):
    frequencies: List[float]
    magnitudes: List[float]
    dominant_frequency: float

class SignalProcessingCapability(ExecutableCapability):
    """
    Capacité de traitement du signal pour calculer la Transformée de Fourier Discrète.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "math.signal_processing",
            "name": "Signal Processing (Fourier Transform)",
            "version": "2.0.0",
            "description": "Computes the Discrete Fourier Transform (DFT) of a signal.",
            "dependencies": ["numpy", "scipy", "pydantic"],
            "input_schema": SignalProcessingParams.model_json_schema(),
            "output_schema": SignalProcessingResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = SignalProcessingParams(**params)
        
        N = len(p.signal)
        yf = fft(p.signal)
        xf = fftfreq(N, 1 / p.sample_rate)
        
        # Ignorer la composante miroir pour trouver la fréquence dominante
        magnitudes = np.abs(yf[:N//2])
        frequencies = xf[:N//2]
        
        dominant_freq = 0.0
        if len(magnitudes) > 0:
            dominant_index = np.argmax(magnitudes)
            dominant_freq = frequencies[dominant_index]

        result = SignalProcessingResult(
            frequencies=xf.tolist(),
            magnitudes=np.abs(yf).tolist(),
            dominant_frequency=dominant_freq
        )
        return result.model_dump()
