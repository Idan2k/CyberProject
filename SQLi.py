class SQLi:
    def __init__(self, URL, parameter, payload_type, payload):
        self.__URL = URL
        self.__parameter = parameter
        self.__payload_type = payload_type
        self.__payload = payload

    def __repr__(self):
        return f'SQLi("{self.__URL}","{self.__parameter}","{self.__payload_type},"{self.__payload}")'

    def __str__(self):
       return f'"{self.__URL}","{self.__parameter}","{self.__payload_type}","{self.__payload}"'

# PROPERTIES (GETTERS ONLY)
    # --------------------------------------------
    # URL PROPERTY
    @property
    # Getter method
    def URL(self):
        return self.__URL

    # --------------------------------------------

    # PARAMETER PROPERTY
    @property
    # Getter method
    def parameter(self):
        return self.__parameter

    # --------------------------------------------

    # PAYLOAD_TYPE PROPERTY
    @property
    # Getter method
    def payload_type(self):
        return self.__payload_type

    # --------------------------------------------

    # PAYLOAD PROPERTY
    @property
    # Getter method
    def version(self):
        return self.__payload
