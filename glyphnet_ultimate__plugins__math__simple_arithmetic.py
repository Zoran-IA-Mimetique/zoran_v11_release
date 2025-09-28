""" Simple Arithmetic plugin """

from ..engines.capabilities import ExecutableCapability
from typing import Dict, Any
class SimpleArithmetic(ExecutableCapability):
    def metadata(self): return {"id":"math.simple_arithmetic"}
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        op=params.get('operation'); a=params.get('a',0); b=params.get('b',0)
        if op=='add': return {'result':a+b}
        if op=='subtract': return {'result':a-b}
        raise ValueError('unsupported op')
