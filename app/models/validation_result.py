from dataclasses import dataclass


@dataclass
class ValidationResult:

    rule_name: str

    column_name: str

    severity: str

    failed_rows: int

    passed: bool

    message: str