import pandas as pd


class IncrementalLoader:

    def __init__(self, db):

        self.db = db
        
        

    def filter_new_records(self, df):

        query = """
        SELECT Order_ID
        FROM bronze_orders
        """

        existing = pd.read_sql(
            query,
            self.db.engine
        )
        print(existing["Order_ID"].dtype)

        if existing.empty:

            return df
        df["Order_ID"] = df["Order_ID"].astype(str)
        existing["Order_ID"] = existing["Order_ID"].astype(str)

        new_df = df[
         ~df["Order_ID"].isin(existing["Order_ID"])
        ]

       

        return new_df