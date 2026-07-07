from pathlib import Path
import yaml
import json

class SchemaValidator:

    def __init__(self, dataframe):

        self.df = dataframe

        schema_file = Path("config/expected_schema.yaml")

        with open(schema_file, "r") as f:

            config = yaml.safe_load(f)

        self.expected_columns = config["expected_columns"]

    def validate(self):

        actual = list(self.df.columns)

        expected = self.expected_columns

        missing = []

        extra = []

        for column in expected:

            if column not in actual:

                missing.append(column)

        for column in actual:

            if column not in expected:

                extra.append(column)

        report = {

            "expected_columns": len(expected),

            "actual_columns": len(actual),

            "missing_columns": missing,

            "unexpected_columns": extra,

            "status": len(missing) == 0 and len(extra) == 0

        }
        with open("reports/schema_report.json", "w") as file:

         json.dump(report, file, indent=4)

        return report