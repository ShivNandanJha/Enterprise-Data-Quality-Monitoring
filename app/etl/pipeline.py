from app.services.audit_service import AuditService
from app.services.quality_service import QualityService
from app.services.run_logger import RunLogger
from database.connection import Database
from app.etl.extract import Extract
from app.etl.transform import Transform
from app.etl.load import Load
from app.profiling.profiler import DataProfiler
from app.validation.schema_validator import SchemaValidator
from app.validation.validator import Validator
from app.profiling.profiler import DataProfiler
from app.profiling.profile_service import ProfileService

class Pipeline:

    def run(self):
        logger = RunLogger()

        logger.start()

        db = Database()

        db.connect()

        df = Extract().run()
        profiles = DataProfiler(df).generate_profile()
        
        ProfileService.save(profiles)

        print("\n========== DATA PROFILE ==========\n")

        for profile in profiles:
            print(profile)
        
        report = SchemaValidator(df).validate()

        print("\n========== SCHEMA VALIDATION ==========\n")

        print(f"Expected Columns : {report['expected_columns']}")

        print(f"Actual Columns   : {report['actual_columns']}")

        print(f"Missing Columns  : {len(report['missing_columns'])}")

        print(f"Extra Columns    : {len(report['unexpected_columns'])}")

        print(f"Status           : {'PASS' if report['status'] else 'FAIL'}")

        if not report["status"]:

           raise Exception("Schema Validation Failed")
        
        # DataProfiler(df).basic_info()
        
        validation_results = Validator(df).run()
        score = QualityService.calculate(validation_results)

        
        passed = sum(r.passed for r in validation_results)
        failed = len(validation_results) - passed
        print("\n" + "=" * 50)
        print("      DATA QUALITY SUMMARY")
        print("=" * 50)
        print(f"Rows Read        : {len(df):,}")
        print(f"Rules Executed   : {len(validation_results)}")
        print(f"Rules Passed     : {passed}")
        print(f"Rules Failed     : {failed}")
        print(f"Quality Score    : {score}%")
        df = Transform().run(df)

        Load(db).run(df)
        duration = logger.stop()

        print(f"Execution Time   : {duration} sec")
        print("=" * 50)
        print(duration)

        summary = {

            "total_rows": len(df),

            "loaded_rows": len(df),

            "rejected_rows": 0,

            "quality_score": score,

            "status": "SUCCESS",

            "duration": duration,

            "remarks": "Pipeline executed successfully"

        }

        AuditService.save(summary)

        db.disconnect()