# -----------------------------
# Service Imports
# -----------------------------
from app.services.audit_service import AuditService
from app.services.quality_service import QualityService
from app.services.run_logger import RunLogger

# -----------------------------
# Database Connection
# -----------------------------
from database.connection import Database

# -----------------------------
# ETL Components
# -----------------------------
from app.etl.extract import Extract
from app.etl.transform import Transform
from app.etl.load import Load
from app.etl.incremental_loader import IncrementalLoader

# -----------------------------
# Profiling Components
# -----------------------------
from app.profiling.profiler import DataProfiler
from app.profiling.profile_service import ProfileService

# -----------------------------
# Validation Components
# -----------------------------
from app.validation.schema_validator import SchemaValidator
from app.validation.validator import Validator

# -----------------------------
# Alert Components
# -----------------------------
from app.alerts.decision_engine import AlertDecisionEngine
from app.alerts.email_template import EmailTemplate
from app.alerts.email_service import EmailService


class Pipeline:
    """
    Main pipeline controller.

    Responsible for executing the complete ETL workflow:

    1. Start logging
    2. Connect database
    3. Extract data
    4. Generate data profile
    5. Validate schema
    6. Execute validation rules
    7. Calculate quality score
    8. Send alerts (if required)
    9. Transform data
    10. Filter incremental records
    11. Load data
    12. Save audit information
    """

    def run(self):

        # -----------------------------------------
        # Start execution timer
        # -----------------------------------------
        logger = RunLogger()
        logger.start()

        # -----------------------------------------
        # Establish database connection
        # -----------------------------------------
        db = Database()
        db.connect()

        # -----------------------------------------
        # Extract source data
        # -----------------------------------------
        df = Extract().run()

        # -----------------------------------------
        # Generate column profiling statistics
        # -----------------------------------------
        profiles = DataProfiler(df).generate_profile()

        # Save profiling information
        ProfileService.save(profiles)

        # -----------------------------------------
        # Validate schema before processing
        # -----------------------------------------
        report = SchemaValidator(df).validate()

        print("\n========== SCHEMA VALIDATION ==========\n")

        print(f"Expected Columns : {report['expected_columns']}")
        print(f"Actual Columns   : {report['actual_columns']}")
        print(f"Missing Columns  : {len(report['missing_columns'])}")
        print(f"Extra Columns    : {len(report['unexpected_columns'])}")
        print(f"Status           : {'PASS' if report['status'] else 'FAIL'}")

        # Stop pipeline immediately if schema fails
        if not report["status"]:
            raise Exception("Schema Validation Failed")

        # -----------------------------------------
        # Execute all configured validation rules
        # -----------------------------------------
        validation_results = Validator(df).run()

        # -----------------------------------------
        # Calculate overall data quality score
        # -----------------------------------------
        score = QualityService.calculate(validation_results)

        # -----------------------------------------
        # Decide whether an alert should be sent
        # -----------------------------------------
        should_send = AlertDecisionEngine.should_send_alert(
            schema_status=report["status"],
            validation_results=validation_results,
            quality_score=score
        )

        # -----------------------------------------
        # Send email alert if required
        # -----------------------------------------
        if should_send:

            html = EmailTemplate.build(
                score,
                validation_results
            )

            EmailService.send(
                subject="🚨 Enterprise Data Quality Alert",
                html=html
            )

        # -----------------------------------------
        # Display validation summary
        # -----------------------------------------
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

        # -----------------------------------------
        # Perform data transformation
        # -----------------------------------------
        df = Transform().run(df)

        # Verify transformed datatype
        print(df["Order_ID"].dtype)

        # -----------------------------------------
        # Perform Incremental Loading
        # Only keep records that don't already exist
        # -----------------------------------------
        incremental_loader = IncrementalLoader(db)

        df = incremental_loader.filter_new_records(df)

        print(f"New Records : {len(df)}")

        # -----------------------------------------
        # Load transformed data into database
        # -----------------------------------------
        Load(db).run(df)

        # -----------------------------------------
        # Stop timer
        # -----------------------------------------
        duration = logger.stop()

        print(f"Execution Time   : {duration} sec")
        print("=" * 50)

        # -----------------------------------------
        # Prepare audit information
        # -----------------------------------------
        summary = {

            "total_rows": len(df),

            "loaded_rows": len(df),

            "rejected_rows": 0,

            "quality_score": score,

            "status": "SUCCESS",

            "duration": duration,

            "remarks": "Pipeline executed successfully"

        }

        # Save execution summary
        AuditService.save(summary)

        # -----------------------------------------
        # Close database connection
        # -----------------------------------------
        db.disconnect()