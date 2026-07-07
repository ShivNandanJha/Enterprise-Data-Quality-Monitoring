import pandas as pd


class Load:

    def __init__(self, db):

        self.db = db

    def run(self, df: pd.DataFrame):

        df.to_sql(
            name="bronze_orders",
            con=self.db.engine,
            if_exists="append",
            index=False,
            chunksize=5000,
            method="multi"
        )

        print("Bronze Loaded Successfully")