from app.validation.rules.base_rule import BaseRule
from app.models.validation_result import ValidationResult


class NotNullRule(BaseRule):

    def validate(self, dataframe):

        failed = dataframe[self.column].isnull().sum()

        return ValidationResult(

         rule_name="Not Null",

         column_name=self.column,

         severity=self.severity,

         failed_rows=int(failed),

         passed=failed == 0,

         message=f"{failed} null values found"

)