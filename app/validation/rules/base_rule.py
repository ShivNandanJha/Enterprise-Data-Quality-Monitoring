from abc import ABC, abstractmethod


class BaseRule(ABC):

    def __init__(self, column, severity="warning"):

        self.column = column
        self.severity = severity

    @abstractmethod
    def validate(self, dataframe):
        pass