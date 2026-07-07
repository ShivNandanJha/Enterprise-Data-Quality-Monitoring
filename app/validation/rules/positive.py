from app.validation.rules.base_rule import BaseRule
from app.models.validation_result import ValidationResult

class PositiveRule(BaseRule):

    def validate(self, dataframe):

        failed = (dataframe[self.column] <= 0).sum()

        return ValidationResult(

            rule_name="Positive",

            column_name=self.column,

            severity=self.severity,

            failed_rows=int(failed),

            passed=failed == 0,

            message=f"{failed} non-positive values found"

        )