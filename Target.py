from datetime import datetime

from Memory import Memory


class Target(object):
    count = 0

    @classmethod
    def set_count(cls, count):
        cls.count = count

    @classmethod
    def incr(cls):
        cls.count += 1
        return cls.count

    def __init__(self, ip):
        self.__id = self.incr()
        # print(self.__id)
        self.__ip = ip
        self.__crt_date = datetime.now()
        self.__scans = []
        self.__opened_ports = []
        self.__filtered_ports = []
        # memory for later upgrade
        # self.__memory = Memory()
        # self.__class__.newid += 1

    # def __del__(self):
        # self.__memory.__del__()
    # def __repr__(self):
    #     # opened_ports = '__opened_ports(asdasd'
    #     # filtered_ports = '__filtered_ports(dsadsa'
    #     # for port in self.__opened_ports:
    #     #     opened_ports += repr(port) + ","
    #     # opened_ports = opened_ports[:-1]
    #     # opened_ports += ')'
    #     # for port in self.__filtered_ports:
    #     #     filtered_ports += repr(port) + ","
    #     # filtered_ports = filtered_ports[:-1]
    #     # filtered_ports += ')'
    #     for port in self.__opened_ports:
    #         print("1" + port)
    #
    #     print("2" + str(self.__opened_ports))
    #     print("3" + repr(self.__opened_ports))
    #     return f'Target("{self.__id}","{self.__ip}","{self.__opened_ports}",{repr(self.__filtered_ports)},"{repr(self.__memory)}")'

    # def __repr__(self):
    #     return f'Target("{self.__id}","{self.__ip}","{self.__opened_ports}","{self.__crt_date}")'
    #
    # def __str__(self):
    #     opened_ports = '__opened_ports('
    #     filtered_ports = '__filtered_ports('
    #     for port in self.__opened_ports:
    #         opened_ports += str(port) + ","
    #     opened_ports = opened_ports[:-1]
    #     opened_ports += ')'
    #     for port in self.__filtered_ports:
    #         filtered_ports += str(port) + ","
    #     filtered_ports = filtered_ports[:-1]
    #     filtered_ports += ')'
    #     return f'"{self.__id}","{self.__ip}","{opened_ports}","{filtered_ports}","{str(self.__memory)}"'

    def get_dict(self, dict_name):
        ret_dict = dict({})
        temp = None
        if dict_name == 'opened':
            temp = self.__opened_ports
        elif dict_name == 'filtered':
            temp = self.__filtered_ports
        if temp is None:
            print("Error Occured")
            exit(-2)
        for port in temp:
            # port_info = str(port).replace("\"", "").split(',')
            ret_dict[port.port_number] = port.protocol + "," + port.service + "," + port.version
        return ret_dict

    # PROPERTIES
    # --------------------------------------------
    # ID PROPERTY
    @property
    # Getter method
    def id(self):
        return self.__id

    # Setter method
    @id.setter
    def id(self, val):
        self.__id = val
    # --------------------------------------------

    # IP PROPERTY
    @property
    # Getter method
    def ip(self):
        return self.__ip

    # Setter method
    @ip.setter
    def ip(self, val):
        self.__ip = val

    # --------------------------------------------

    # OPENED PORTS PROPERTY
    @property
    # Getter method
    def opened_ports(self):
        return self.__opened_ports

    # Setter method
    @opened_ports.setter
    def opened_ports(self, val):
        self.__opened_ports = val

    # --------------------------------------------

    # FILTERED PORTS PROPERTY
    @property
    # Getter method
    def filtered_ports(self):
        return self.__filtered_ports

    # Setter method
    @filtered_ports.setter
    def filtered_ports(self, val):
        self.__filtered_ports = val

    # --------------------------------------------

    # MEMORY PROPERTY
    @property
    # Getter method
    def memory(self):
        return self.__memory

    # Setter method
    @memory.setter
    def memory(self, val):
        self.__memory = val

    # --------------------------------------------

    # SCANS PROPERTY
    @property
    # Getter method
    def scans(self):
        return self.__scans

    # Setter method
    @scans.setter
    def scans(self, val):
        self.__scans = val

    # --------------------------------------------

    # CREATION DATE PROPERTY
    @property
    # Getter method
    def crt_date(self):
        return self.__crt_date

    # Setter method
    @crt_date.setter
    def crt_date(self, val):
        self.__crt_date = val

