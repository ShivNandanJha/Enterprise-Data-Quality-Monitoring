from app.services.quality_service import QualityService
from database.connection import Database
from app.etl.extract import Extract
from app.etl.transform import Transform
from app.etl.load import Load
from app.profiling.profiler import DataProfiler
from app.validation.schema_validator import SchemaValidator
from app.validation.validator import Validator

class Pipeline:

    def run(self):

        db = Database()

        db.connect()

        df = Extract().run()
        report = SchemaValidator(df).validate()

        print("\n========== SCHEMA VALIDATION ==========\n")

        print(f"Expected Columns : {report['expected_columns']}")

        print(f"Actual Columns   : {report['actual_columns']}")

        print(f"Missing Columns  : {len(report['missing_columns'])}")

        print(f"Extra Columns    : {len(report['unexpected_columns'])}")

        print(f"Status           : {'PASS' if report['status'] else 'FAIL'}")

        if not report["status"]:

           raise Exception("Schema Validation Failed")
        
        DataProfiler(df).basic_info()
        
        results = Validator(df).run()
        score = QualityService.calculate(results)

        print(f"Quality Score: {score}")

        df = Transform().run(df)

        Load(db).run(df)

        db.disconnect()