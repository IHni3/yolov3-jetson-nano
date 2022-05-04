#for terminal colors
from termcolor import colored, cprint

# logging constants
__INFO = "[INFO]:" 
__ERROR = "[ERROR]:"
__SUCCESS = "[SUCCESS]:"
__DEBUG = "[DEBUG]:"

# color constants
__COLOR_RED = "red"
__COLOR_GREEN = "green"

# enable or disable verbose printing
enable_verbose_output = False

# printing functions
def error(message):
    cprint(__ERROR + " " + message, __COLOR_RED)

def info(message):
    print(__INFO, message)

def success(message):
    if not printOnlyErrors:
        cprint(__SUCCESS + " " +  message, __COLOR_GREEN)

def verbose(message):
    if enable_verbose_output:
        print(__DEBUG, message)