import numpy as np
from typing import Dict, Any, List
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class FractalParams(BaseModel):
    width: int = Field(50, gt=1, le=512)
    height: int = Field(50, gt=1, le=512)
    max_iterations: int = Field(50, gt=1, le=1000)

class FractalResult(BaseModel):
    iteration_matrix: List[List[int]]

class FractalCapability(ExecutableCapability):
    """
    Capacité de génération de l'ensemble de Mandelbrot.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "math.fractal_generator",
            "name": "Mandelbrot Set Generator",
            "version": "2.0.0",
            "description": "Generates the iteration matrix for a visualization of the Mandelbrot set.",
            "dependencies": ["numpy", "pydantic"],
            "input_schema": FractalParams.model_json_schema(),
            "output_schema": FractalResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = FractalParams(**params)
        
        re_coords = np.linspace(-2.0, 1.0, p.width)
        im_coords = np.linspace(-1.5, 1.5, p.height)
        
        result_matrix = np.zeros((p.height, p.width), dtype=int)

        for i in range(p.height):
            for j in range(p.width):
                c = re_coords[j] + 1j * im_coords[i]
                z = 0
                n = 0
                while abs(z) <= 2 and n < p.max_iterations:
                    z = z*z + c
                    n += 1
                result_matrix[i, j] = n
        
        result = FractalResult(iteration_matrix=result_matrix.tolist())
        return result.model_dump()
