import yaml

from app.services.rule_factory import RuleFactory


class Validator:
    """
    Executes all data validation rules defined
    in the rules.yaml configuration file.
    """

    def __init__(self, dataframe):
        """
        Initialize the Validator.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Dataset on which validation rules
            will be executed.
        """

        # Store the input dataset
        self.df = dataframe

        # -----------------------------------------
        # Load validation rules from YAML
        # -----------------------------------------
        with open("config/rules.yaml") as file:

            self.rules = yaml.safe_load(file)["rules"]

    def run(self):
        """
        Execute every validation rule.

        Returns
        -------
        list
            List of ValidationResult objects.
        """

        # Store validation results
        results = []

        # -----------------------------------------
        # Execute each configured rule
        # -----------------------------------------
        for rule in self.rules:

            # Create appropriate validator
            validator = RuleFactory.create(rule)

            # Execute validation
            results.append(

                validator.validate(self.df)

            )

        # Return all validation results
        return results