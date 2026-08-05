from dataclasses import dataclass


@dataclass(slots=True)
class ValidationIssue:
    validator: str
    severity: str
    type: str
    source: str
    target: str
    message: str
