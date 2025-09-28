import numpy as np
from typing import Dict, Any, List
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class NeuroSpikeParams(BaseModel):
    input_currents: conlist(float, min_length=1)
    membrane_threshold: float = Field(1.0, gt=0)
    membrane_potential_decay: float = Field(0.9, ge=0, lt=1)
    reset_potential: float = Field(0.0)

class NeuroSpikeResult(BaseModel):
    spike_train: List[int]
    membrane_potential_trace: List[float]

class NeuroSpikeCapability(ExecutableCapability):
    """
    Simule un neurone Leaky Integrate-and-Fire (LIF), un modèle de base
    pour les réseaux de neurones à impulsions (spiking neural networks).
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "neuro.lif_neuron_simulation",
            "name": "Leaky Integrate-and-Fire Neuron",
            "version": "2.0.0",
            "description": "Simulates a Leaky Integrate-and-Fire (LIF) neuron model.",
            "dependencies": ["numpy", "pydantic"],
            "input_schema": NeuroSpikeParams.model_json_schema(),
            "output_schema": NeuroSpikeResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = NeuroSpikeParams(**params)
        
        potential = 0.0
        spikes = []
        potential_trace = []

        for current in p.input_currents:
            # Intégration avec fuite (Leaky Integration)
            potential = potential * p.membrane_potential_decay + current
            
            # Déclenchement (Fire)
            if potential >= p.membrane_threshold:
                spikes.append(1)
                potential = p.reset_potential # Réinitialisation du potentiel
            else:
                spikes.append(0)
            
            potential_trace.append(potential)
            
        result = NeuroSpikeResult(
            spike_train=spikes,
            membrane_potential_trace=potential_trace
        )
        return result.model_dump()
