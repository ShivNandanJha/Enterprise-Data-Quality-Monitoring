import uuid

from database.connection import Database


class AuditService:

    @staticmethod
    def _ensure_pipeline_runs_schema(cursor):

        cursor.execute(
            """
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'pipeline_runs'
            """
        )

        existing_columns = {row[0] for row in cursor.fetchall()}

        required_columns = {
            "total_rows": "INT",
            "loaded_rows": "INT",
            "rejected_rows": "INT",
            "quality_score": "DECIMAL(5,2)",
            "execution_status": "VARCHAR(20)",
            "execution_duration": "DOUBLE",
            "remarks": "TEXT",
        }

        for column_name, column_type in required_columns.items():

            if column_name not in existing_columns:

                cursor.execute(
                    f"ALTER TABLE pipeline_runs ADD COLUMN {column_name} {column_type}"
                )

    @staticmethod
    def _get_pipeline_runs_columns(cursor):

        cursor.execute(
            """
            SELECT COLUMN_NAME, DATA_TYPE, EXTRA
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'pipeline_runs'
            """
        )

        return {
            row[0]: {"data_type": row[1], "extra": row[2] or ""}
            for row in cursor.fetchall()
        }

    @staticmethod
    def save(summary):

        db = Database()
        db.connect()

        cursor = db.connection.cursor()

        AuditService._ensure_pipeline_runs_schema(cursor)
        columns = AuditService._get_pipeline_runs_columns(cursor)

        insert_columns = []
        insert_values = []

        run_id_meta = columns.get("run_id")

        if run_id_meta and "auto_increment" not in run_id_meta["extra"].lower():

            insert_columns.append("run_id")
            insert_values.append(str(uuid.uuid4()))

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

        for column_name, value in field_mappings:

            if column_name in columns:

                insert_columns.append(column_name)
                insert_values.append(value)

        query = """
        INSERT INTO pipeline_runs
        ({columns})
        VALUES ({placeholders})
        """

        query = query.format(
            columns=", ".join(insert_columns),
            placeholders=", ".join(["%s"] * len(insert_columns)),
        )

        cursor.execute(query, tuple(insert_values))

        db.connection.commit()

        cursor.close()
        db.disconnect()