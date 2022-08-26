import itertools
from datetime import datetime


class Scan:
    count = 0

    @classmethod
    def set_count(cls, count):
        cls.count = count

    @classmethod
    def incr(cls):
        cls.count += 1
        return cls.count

    def __init__(self):
        self.__id = self.incr()
        self.__crt_date = datetime.now()
        self.__reports = dict({})

    # def __repr__(self):
    #     results = ''
    #     for key in self.__results:
    #         results +=
    #     return f'Target("{self.__id}","{self.__crt_date}")'

    # def __repr__(self):
    #     return f'"{self.__id}","{self.__crt_date}","{self.__reports}"'
    #
    # def __str__(self):
    #     pass

# PROPERTIES
    # --------------------------------------------
    # ID PROPERTY
    @property
    # Getter method
    def id(self):
        return self.__id

    # --------------------------------------------

    # CREATION DATE PROPERTY
    @property
    # Getter method
    def crt_date(self):
        return self.__crt_date

    # --------------------------------------------

    # RESULTS DICT PROPERTY
    @property
    # Getter method
    def reports(self):
        return self.__reports
