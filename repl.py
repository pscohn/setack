import os
import readline

from colorprint import *
from vm         import VM

historyFilepath = os.path.expanduser('~/.setack_history')

startupMessage = '{}{}'.format(cformat('''
   (                                )  
   )\ )     *   )   (       (    ( /(  
  (()/((  ` )  /(   )\      )\   )\()) 
   /(_))\  ( )(_)|(((_)(  (((_)|((_)\  
  (_))((_)(_(_()) )\ _ )\ )\___|_ ((_)  ''', Color.Red), cformat('''
  / __| __|_   _| (_)_\(_|(/ __| |/ /  
  \__ \ _|  | |    / _ \  | (__  ' <   
  |___/___| |_|   /_/ \_\  \___|_|\_\ 
''', Color.Yellow))

def getFiles():
    result = set()
    cwd    = os.getcwd()
    for directory, _, files in os.walk(cwd):
        for filename in files:
            rel_dir  = os.path.relpath(directory, cwd)
            if rel_dir == '.':
                rel_file = filename
            else:
                rel_file = os.path.join(rel_dir, filename)
            result.add(rel_file)
    return result

class AutoComplete():

    def __init__(self):
        self.options = []

    def add(self, option):
        self.options = sorted(self.options + [option])

    def addOptions(self, options):
        self.options = sorted(self.options + list(options))

    def complete(self, text, state):
        result = None
        if state == 0:
            if not text:
                self.matches = self.options[:]
            else:
                self.matches = [s for s in self.options if s and s.startswith(text)]

        if state < len(self.matches):
            result = self.matches[state]

        return result

def run():

    # Configure readline history
    if not os.path.exists(historyFilepath): 
        open(historyFilepath, 'w')
    readline.read_history_file(historyFilepath)

    # Configure readline autocomplete
    autoComplete = AutoComplete()

    autoComplete.addOptions(getFiles())

    readline.set_completer_delims(' \t"')
    readline.parse_and_bind('tab: complete')
    readline.set_completer(autoComplete.complete)

    try:
        vm = VM(autoComplete)
        print(startupMessage)
        while True:
            line = input(cformat('> ', Color.Green))
            try:
                r = vm.eval(line)
                if r:
                    print(r)
            except Exception as e:
                eType    = type(e)
                eMessage = ''
                if eType == SyntaxError:
                    eMessage += e.text + '\n'
                    eMessage += ' ' * e.offset + cformat('^', Color.Red) + '\n'
                eMessage += cformat(eType.__name__ + ': ', Color.Magenta)
                eMessage += cformat(e, Color.Cyan)
                print(eMessage)
    except (KeyboardInterrupt, EOFError):
        exit(0)
    finally:
        readline.write_history_file(historyFilepath)

