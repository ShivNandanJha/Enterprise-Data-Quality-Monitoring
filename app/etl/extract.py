from pathlib import Path

import pandas as pd


class Extract:

    def __init__(self):

        self.path = Path("data/raw/orders.csv")

    def run(self):

        df = pd.read_csv(self.path)

        print(f"Rows : {len(df)}")

        print(f"Columns : {len(df.columns)}")

        return df