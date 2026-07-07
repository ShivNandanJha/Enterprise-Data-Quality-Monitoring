from app.validation.rules.not_null import NotNullRule
from app.validation.rules.unique import UniqueRule
from app.validation.rules.positive import PositiveRule
from app.validation.rules.range_rule import RangeRule


class RuleFactory:

    @staticmethod
    def create(rule):

        rule_type = rule["type"]

        if rule_type == "not_null":

            return NotNullRule(

                rule["column"],

                rule["severity"]

            )

        elif rule_type == "unique":

            return UniqueRule(

                rule["column"],

                rule["severity"]

            )

        elif rule_type == "positive":

            return PositiveRule(

                rule["column"],

                rule["severity"]

            )

        elif rule_type == "range":

            return RangeRule(

                rule["column"],

                rule["min"],

                rule["max"],

                rule["severity"]

            )

        else:

            raise Exception(f"Unknown Rule {rule_type}")