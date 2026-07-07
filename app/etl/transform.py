import pandas as pd


class Transform:

    def run(self, df: pd.DataFrame):

        df.columns = (
            df.columns
            .str.strip()
            .str.replace(" ", "_")
        )

        return df