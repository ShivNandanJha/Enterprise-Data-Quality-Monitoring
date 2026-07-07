from app.validation.rules.base_rule import BaseRule
from app.models.validation_result import ValidationResult


class UniqueRule(BaseRule):

    def validate(self, dataframe):

        failed = dataframe[self.column].duplicated().sum()

        return ValidationResult(

            rule_name="Unique",

            column_name=self.column,

            failed_rows=int(failed),

            passed=failed == 0,

            severity=self.severity,
            message=f"{failed} duplicate values found"

        )