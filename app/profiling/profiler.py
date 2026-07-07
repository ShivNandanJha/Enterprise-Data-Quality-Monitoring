import pandas as pd


class DataProfiler:

    def __init__(self, dataframe):
        self.df = dataframe

    def generate_profile(self):

        profiles = []

        for column in self.df.columns:

            profile = {
                "column_name": column,
                "data_type": str(self.df[column].dtype),
                "total_rows": int(len(self.df)),
                "null_count": int(self.df[column].isnull().sum()),
                "null_percentage":float(round(
                    self.df[column].isnull().mean() * 100,
                    2
                )),
                "unique_values": int(
                    self.df[column].nunique()
                )
            }

            # Numeric columns
            if pd.api.types.is_numeric_dtype(self.df[column]):

                profile["min"] =float(self.df[column].min())
                profile["max"] = float(self.df[column].max())
                profile["mean"] = float(round(
                    self.df[column].mean(),
                    2
                ))

            else:

                profile["min"] = None
                profile["max"] = None
                profile["mean"] = None

            profiles.append(profile)

        return profiles