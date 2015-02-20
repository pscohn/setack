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

keywords = '''
    depth in show-stack clear symmetric-difference not-in subset union
    power-set difference cartesian-product drop intersection show-symbols
'''

class AutoComplete():

    def __init__(self, options):
        optionsType = type(options)
        if optionsType is list:
            self.options = sorted(options)
        elif optionsType is str:
            self.options = sorted(options.split())
        else:
            raise ValueError('options must be a list or str')

    def complete(self, text, state):
        result = None
        if state == 0:
            if not text:
                self.matches = self.options[:]
            else:
                self.matches = [s for s in self.options if s and s.startswith(text)]
        if state < len(self.matches):
            result = self.matches[state] + ' '
        return result

def run():

    # Configure readline history
    if not os.path.exists(historyFilepath): 
        open(historyFilepath, 'w')
    readline.read_history_file(historyFilepath)

    # Configure readline autocomplete
    autoComplete = AutoComplete(keywords)
    readline.set_completer_delims('\t')
    readline.set_completer(autoComplete.complete)
    readline.parse_and_bind('tab: complete')

    try:
        vm = VM()
        print(startupMessage)
        while True:
            line = input(cformat('> ', Color.Green))
            try:
                vm.eval(line)
            except Exception as e:
                eType    = type(e)
                eMessage = ''
                if eType == SyntaxError:
                    eMessage += e.text + '\n'
                    eMessage += ' ' * e.offset + cformat('^', Color.Red) + '\n'
                eMessage += cformat(eType.__name__ + ':', Color.Magenta)
                eMessage += cformat(e, Color.Cyan)
                print(eMessage)
    except (KeyboardInterrupt, EOFError):
        exit(0)
    finally:
        readline.write_history_file(historyFilepath)

