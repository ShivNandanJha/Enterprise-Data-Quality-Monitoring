import pandas as pd


class DataProfiler:

    def __init__(self, df):

        self.df = df

    def basic_info(self):

        print("\n========== DATA PROFILE ==========\n")

        print(f"Rows : {self.df.shape[0]}")

        print(f"Columns : {self.df.shape[1]}")

        print("\nColumn Types\n")

        print(self.df.dtypes)

        print("\nMissing Values\n")

        print(self.df.isnull().sum())

        print("\nDuplicate Rows")

        print(self.df.duplicated().sum())