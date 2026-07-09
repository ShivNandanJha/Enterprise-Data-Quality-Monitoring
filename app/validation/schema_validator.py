from pathlib import Path
import yaml
import json


class SchemaValidator:
    """
    Validates whether the incoming dataset matches
    the expected schema defined in a YAML file.
    """

    def __init__(self, dataframe):
        """
        Initialize the Schema Validator.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Input dataset whose schema needs validation.
        """

        # Store input DataFrame
        self.df = dataframe

        # Path to expected schema configuration
        schema_file = Path("config/expected_schema.yaml")

        # Load expected schema from YAML file
        with open(schema_file, "r") as f:
            config = yaml.safe_load(f)

        # Extract expected column names
        self.expected_columns = config["expected_columns"]

    def validate(self):
        """
        Compare actual dataset columns with expected columns.

        Returns
        -------
        dict
            Validation report containing:
            - Expected columns count
            - Actual columns count
            - Missing columns
            - Unexpected columns
            - Validation status
        """

        # Actual column names from DataFrame
        actual = list(self.df.columns)

        # Expected column names from YAML
        expected = self.expected_columns

        # Lists to store mismatches
        missing = []
        extra = []

        # -----------------------------------------
        # Find missing columns
        # -----------------------------------------
        for column in expected:

            if column not in actual:

                missing.append(column)

        # -----------------------------------------
        # Find unexpected columns
        # -----------------------------------------
        for column in actual:

            if column not in expected:

                extra.append(column)

        # -----------------------------------------
        # Prepare validation report
        # -----------------------------------------
        report = {

            "expected_columns": len(expected),

            "actual_columns": len(actual),

            "missing_columns": missing,

            "unexpected_columns": extra,

            # Validation passes only if
            # no missing and no extra columns exist
            "status": (
                len(missing) == 0
                and
                len(extra) == 0
            )

        }

        # Save report as JSON
        with open(
            "reports/schema_report.json",
            "w"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        return report