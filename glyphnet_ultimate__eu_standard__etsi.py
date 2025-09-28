""" ETSI Compliance Checker (minimal) """

from typing import List
from pydantic import BaseModel
class Finding(BaseModel):
    compliant: bool
    message: str
    requirement_id: str
class SpecResult(BaseModel):
    spec_id: str
    is_fully_compliant: bool
    findings: List[Finding]
def check_minimal(model) -> List[SpecResult]:
    f = [Finding(compliant=bool(model.signature), message="Model must be signed.", requirement_id="1.1")]
    return [SpecResult(spec_id="ETSI TS 103 645", is_fully_compliant=all(x.compliant for x in f), findings=f)]
