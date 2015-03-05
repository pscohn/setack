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

def findFilesInCurrentDirectory():
    result = []
    cwd    = os.getcwd()
    for directory, _, files in os.walk(cwd):
        for filename in files:
            rel_dir = os.path.relpath(directory, cwd)
            if rel_dir == '.':
                rel_file = filename
            else:
                rel_file = os.path.join(rel_dir, filename)
            result.append(rel_file)
    return result

class AutoComplete():
    def __init__(self):
        self.options = []
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

def formatException(e):
    result = ''
    eType  = type(e)
    if eType == SyntaxError:
        result += e.text + '\n'
        result += ' ' * e.offset + cformat('^', Color.Red) + '\n'
    result += cformat(eType.__name__ + ': ', Color.Magenta)
    result += cformat(e, Color.Cyan)
    return result

def run():

    vm = VM()

    if not os.path.exists(historyFilepath): 
        open(historyFilepath, 'w')
    readline.read_history_file(historyFilepath)

    autoComplete = AutoComplete()
    autoComplete.addOptions(findFilesInCurrentDirectory())
    autoComplete.addOptions(vm.symbols.keys())
    readline.set_completer(autoComplete.complete)
    readline.set_completer_delims(' \t"')
    readline.parse_and_bind('tab: complete')

    try:
        print(startupMessage)
        while True:
            line = input(cformat('> ', Color.Green))
            try:
                result = vm.eval(line)
                if result: 
                    print(result)
            except Exception as e:
                print(formatException(e))
    except (KeyboardInterrupt, EOFError):
        exit(0)
    finally:
        readline.write_history_file(historyFilepath)

