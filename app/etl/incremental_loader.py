import pandas as pd


class IncrementalLoader:
    """
    Filters out records that already exist in the target database.

    Only new records are returned for loading.
    """

    def __init__(self, db):
        """
        Initialize the Incremental Loader.

        Parameters
        ----------
        db : Database
            Database connection object.
        """

        # Store database connection
        self.db = db

    def filter_new_records(self, df):
        """
        Return only records that do not already exist
        in the Bronze table.

        Parameters
        ----------
        df : pandas.DataFrame
            Incoming source data.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing only new records.
        """

        # -----------------------------------------
        # Retrieve all existing Order IDs
        # from Bronze table
        # -----------------------------------------
        query = """
        SELECT Order_ID
        FROM bronze_orders
        """

        existing = pd.read_sql(
            query,
            self.db.engine
        )

        print(existing["Order_ID"].dtype)

        # -----------------------------------------
        # If Bronze table is empty,
        # load all incoming records
        # -----------------------------------------
        if existing.empty:
            return df

        # -----------------------------------------
        # Convert both columns to string
        # to ensure datatype consistency
        # -----------------------------------------
        df["Order_ID"] = df["Order_ID"].astype(str)
        existing["Order_ID"] = existing["Order_ID"].astype(str)

        # -----------------------------------------
        # Keep only records whose Order_ID
        # is NOT present in Bronze table
        # -----------------------------------------
        new_df = df[
            ~df["Order_ID"].isin(existing["Order_ID"])
        ]

        return new_df