from app.validation.rules.base_rule import BaseRule
from app.models.validation_result import ValidationResult


class RangeRule(BaseRule):

    def __init__(self, column, minimum, maximum, severity="warning"):

        super().__init__(column, severity)

        self.minimum = minimum

        self.maximum = maximum

    def validate(self, dataframe):

        failed = (

            (dataframe[self.column] < self.minimum)

            |

            (dataframe[self.column] > self.maximum)

        ).sum()

        return ValidationResult(

            rule_name="Range",

            column_name=self.column,

            failed_rows=int(failed),

            passed=failed == 0,

            severity=self.severity,

            message=f"{failed} values outside the specified range"

        )