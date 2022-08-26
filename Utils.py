import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_ok(content):
    safe_print(bcolors.OKGREEN + bcolors.BOLD + content + bcolors.ENDC)


def print_fail(content):
    safe_print(bcolors.FAIL + bcolors.BOLD + content + bcolors.ENDC)


def print_blue(content):
    safe_print(bcolors.OKBLUE + bcolors.BOLD + content + bcolors.ENDC)


def print_warning(content):
    safe_print(bcolors.WARNING + bcolors.BOLD + content + bcolors.ENDC)


def print_cyan(content):
    safe_print(bcolors.OKCYAN + bcolors.BOLD + content + bcolors.ENDC)


def print_header(content):
    safe_print(bcolors.HEADER + content + bcolors.ENDC)


def safe_print(content):
    # event.clear()
    sys.stdout.write('\r')
    sys.stdout.flush()
    # time.sleep(0.2)
    sys.stdout.write('\r')
    sys.stdout.flush()
    print(content)
    # event.set()

