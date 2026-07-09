import uuid

from database.connection import Database


class AuditService:
    """
    Service responsible for storing pipeline execution
    details into the pipeline_runs table.
    """

    @staticmethod
    def _ensure_pipeline_runs_schema(cursor):
        """
        Ensure that all required columns exist in the
        pipeline_runs table.

        If any required column is missing,
        it will be added automatically.
        """

        # Retrieve existing column names
        cursor.execute("""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'pipeline_runs'
        """)

        existing_columns = {
            row[0]
            for row in cursor.fetchall()
        }

        # Required schema
        required_columns = {

            "total_rows": "INT",

            "loaded_rows": "INT",

            "rejected_rows": "INT",

            "quality_score": "DECIMAL(5,2)",

            "execution_status": "VARCHAR(20)",

            "execution_duration": "DOUBLE",

            "remarks": "TEXT",
        }

        # Add missing columns
        for column_name, column_type in required_columns.items():

            if column_name not in existing_columns:

                cursor.execute(
                    f"""
                    ALTER TABLE pipeline_runs
                    ADD COLUMN {column_name} {column_type}
                    """
                )

    @staticmethod
    def _get_pipeline_runs_columns(cursor):
        """
        Fetch metadata about all columns
        in pipeline_runs.
        """

        cursor.execute("""
            SELECT COLUMN_NAME,
                   DATA_TYPE,
                   EXTRA
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'pipeline_runs'
        """)

        return {

            row[0]: {

                "data_type": row[1],

                "extra": row[2] or ""

            }

            for row in cursor.fetchall()

        }

    @staticmethod
    def save(summary):
        """
        Save pipeline execution summary.

        Parameters
        ----------
        summary : dict
            Contains execution statistics.
        """

        # Connect database
        db = Database()
        db.connect()

        cursor = db.connection.cursor()

        # Ensure schema is updated
        AuditService._ensure_pipeline_runs_schema(cursor)

        # Read latest table structure
        columns = AuditService._get_pipeline_runs_columns(cursor)

        insert_columns = []
        insert_values = []

        # Check whether run_id is AUTO_INCREMENT
        run_id_meta = columns.get("run_id")

        if (
            run_id_meta
            and "auto_increment"
            not in run_id_meta["extra"].lower()
        ):

            insert_columns.append("run_id")

            insert_values.append(
                str(uuid.uuid4())
            )

        # Map application fields
        field_mappings = [

            ("total_rows", summary["total_rows"]),

            ("loaded_rows", summary["loaded_rows"]),

            ("rejected_rows", summary["rejected_rows"]),

            ("quality_score", summary["quality_score"]),

            ("execution_status", summary["status"]),

            ("status", summary["status"]),

            ("execution_duration", summary["duration"]),

            ("duration_seconds", summary["duration"]),

            ("remarks", summary["remarks"]),
        ]

        # Only insert columns that exist
        for column_name, value in field_mappings:

            if column_name in columns:

                insert_columns.append(column_name)

                insert_values.append(value)

        # Dynamic INSERT statement
        query = """
        INSERT INTO pipeline_runs
        ({columns})
        VALUES ({placeholders})
        """

        query = query.format(

            columns=", ".join(insert_columns),

            placeholders=", ".join(
                ["%s"] * len(insert_columns)
            )

        )

        # Execute INSERT
        cursor.execute(
            query,
            tuple(insert_values)
        )

        # Save transaction
        db.connection.commit()

        # Cleanup
        cursor.close()
        db.disconnect()