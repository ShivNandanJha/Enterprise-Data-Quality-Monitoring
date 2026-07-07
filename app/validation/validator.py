import yaml

from app.services.rule_factory import RuleFactory


class Validator:

    def __init__(self, dataframe):

        self.df = dataframe

        with open("config/rules.yaml") as file:

            self.rules = yaml.safe_load(file)["rules"]

    def run(self):

        results = []

        for rule in self.rules:

            validator = RuleFactory.create(rule)

            results.append(

                validator.validate(self.df)

            )

        return results