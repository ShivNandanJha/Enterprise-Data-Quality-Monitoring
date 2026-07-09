import pandas as pd


class DataProfiler:
    """
    Generates profiling statistics for each column
    in a Pandas DataFrame.
    """

    def __init__(self, dataframe):
        """
        Initialize the profiler.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Input dataset to be profiled.
        """

        # Store dataframe for later use
        self.df = dataframe

    def generate_profile(self):
        """
        Generate profiling statistics for every column.

        Returns
        -------
        list
            A list of dictionaries, where each dictionary
            contains profiling information for one column.
        """

        # Store profile of every column
        profiles = []

        # Iterate through every column
        for column in self.df.columns:

            # Basic profiling information
            profile = {

                # Column name
                "column_name": column,

                # Data type of column
                "data_type": str(self.df[column].dtype),

                # Total number of rows
                "total_rows": int(len(self.df)),

                # Count of missing values
                "null_count": int(
                    self.df[column].isnull().sum()
                ),

                # Percentage of missing values
                "null_percentage": float(
                    round(
                        self.df[column].isnull().mean() * 100,
                        2
                    )
                ),

                # Number of unique values
                "unique_values": int(
                    self.df[column].nunique()
                )
            }

            # -----------------------------------------
            # Calculate statistics for numeric columns
            # -----------------------------------------
            if pd.api.types.is_numeric_dtype(self.df[column]):

                # Minimum value
                profile["min"] = float(
                    self.df[column].min()
                )

                # Maximum value
                profile["max"] = float(
                    self.df[column].max()
                )

                # Average value
                profile["mean"] = float(
                    round(
                        self.df[column].mean(),
                        2
                    )
                )

            else:

                # Non-numeric columns
                profile["min"] = None
                profile["max"] = None
                profile["mean"] = None

            # Store profile
            profiles.append(profile)

        # Return profiling report
        return profiles