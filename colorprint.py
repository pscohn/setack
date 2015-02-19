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

esc    = '\033['
reset  = esc + '0m'
colors = { Color.Black  : esc + '30m'
         , Color.Red    : esc + '31m'
         , Color.Green  : esc + '32m'
         , Color.Yellow : esc + '33m'
         , Color.Blue   : esc + '34m'
         , Color.Magenta: esc + '35m'
         , Color.Cyan   : esc + '36m'
         , Color.White  : esc + '37m' }

def cprint (obj, color):
    code = colors.get(color)
    print(code + str(obj) + reset if code else text)

def cformat(obj, color):
    code = colors.get(color)
    return code + str(obj) + reset if code else text

