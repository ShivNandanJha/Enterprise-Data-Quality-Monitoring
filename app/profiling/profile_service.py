from database.connection import Database


class ProfileService:

    @staticmethod
    def save(profiles):

        db = Database()
        db.connect()

        cursor = db.connection.cursor()

        query = """
        INSERT INTO data_profile
        (
            column_name,
            data_type,
            total_rows,
            null_count,
            null_percentage,
            unique_values,
            minimum_value,
            maximum_value,
            average_value
        )

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        for profile in profiles:

            cursor.execute(

                query,

                (

                    profile["column_name"],

                    profile["data_type"],

                    profile["total_rows"],

                    profile["null_count"],

                    profile["null_percentage"],

                    profile["unique_values"],

                    profile["min"],

                    profile["max"],

                    profile["mean"]

                )

            )

        db.connection.commit()

        cursor.close()

        db.disconnect()