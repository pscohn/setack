import enum

class Color(enum.Enum):
    Black   = 0
    Red     = 1
    Green   = 2
    Yellow  = 3
    Blue    = 4
    Magenta = 5
    Cyan    = 6
    White   = 7
    Reset   = 8

colorCode = { Color.Black  : '\033[30m',
              Color.Red    : '\033[31m',
              Color.Green  : '\033[32m',
              Color.Yellow : '\033[33m',
              Color.Blue   : '\033[34m',
              Color.Magenta: '\033[35m',
              Color.Cyan   : '\033[36m',
              Color.White  : '\033[37m',
              Color.Reset  : '\033[0m' }

def cformat(obj, color):
    return colorCode[color] + str(obj) + colorCode[Color.Reset]

def cprint (obj, color):
    print(cformat(obj, color))

