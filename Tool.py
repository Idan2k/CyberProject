import subprocess
from Utils import bcolors


class Tool:
    def __init__(self, name, *args, **kwargs):
        self.__name = name
        self.__args = args
        self.__kwargs = kwargs
        self.__process_id = -1

    # PROPERTIES
    # --------------------------------------------
    # NAME PROPERTY
    @property
    # Getter method
    def name(self):
        return self.__name
    #
    # # Setter method
    # @name.setter
    # def name(self, val):
    #     self.__name = val

    # --------------------------------------------

    # ARGS PROPERTY
    @property
    # Getter method
    def args(self):
        return self.__args

    # Setter method
    @args.setter
    def args(self, val):
        self.__args = val

    # --------------------------------------------
    # KWARGS PROPERTY
    @property
    # Getter method
    def kwargs(self):
        return self.__kwargs

    # Setter method
    @kwargs.setter
    def kwargs(self, val):
        self.__kwargs = val

    # --------------------------------------------
    # PROCESSID PROPERTY
    @property
    # Getter method
    def process_id(self):
        return self.__process_id

    # Setter method
    @process_id.setter
    def process_id(self, val):
        self.__process_id = val

    def run_and_parse_results(self, *command):
        print(bcolors.OKBLUE + bcolors.BOLD + "Launching " + self.name + bcolors.ENDC)
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        done_flag = 0
        out = proc.stdout
        line = out.readline().decode("utf-8").strip("\n")
        while line:
            # event.set()
            print(line)
            # event.clear()
            # time.sleep(0.1)
            line = out.readline().decode("utf-8").strip("\n")



