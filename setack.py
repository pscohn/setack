#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import readline
import vm

from colorprint import *

class MyCompleter(object):  # Custom completer

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if not text:
                self.matches = self.options[:]
            else:
                self.matches = [s for s in self.options
                                if s and s.startswith(text)]

        # return match indexed by state
        try:
            return self.matches[state]
        except IndexError:
            return None

    def display_matches(self, substitution, matches, longest_match_length):
        line_buffer = readline.get_line_buffer()
        columns = environ.get("COLUMNS", 80)

        print()

        tpl = "{:<" + str(int(max(map(len, matches)) * 1.2)) + "}"

        buffer = ""
        for match in matches:
            match = tpl.format(match[len(substitution):])
            if len(buffer + match) > columns:
                print(buffer)
                buffer = ""
            buffer += match

        if buffer:
            print(buffer)

        print("> ", end="")
        print(line_buffer, end="")
        sys.stdout.flush()

history = '{}/{}'.format(os.path.expanduser('~'), '.setack_history')
vm = vm.VM()

if not os.path.exists(history):
    open(history, 'w')

readline.read_history_file(history)

keywords = '''
    depth in show-stack clear symmetric-difference not-in subset ! union
    . power-set difference cartesian-product drop intersection show-symbols
'''.split()
completer = MyCompleter(keywords)

readline.set_completer_delims(' \t\n;')
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')
readline.set_completion_display_matches_hook(completer.display_matches)

try:

    print(cformat('''
   (                                )  
   )\ )     *   )   (       (    ( /(  
  (()/((  ` )  /(   )\      )\   )\()) 
   /(_))\  ( )(_)|(((_)(  (((_)|((_)\  
  (_))((_)(_(_()) )\ _ )\ )\___|_ ((_) ''', Color.Red))
    print(cformat('''  / __| __|_   _| (_)_\(_|(/ __| |/ /  
  \__ \ _|  | |    / _ \  | (__  ' <   
  |___/___| |_|   /_/ \_\  \___|_|\_\ 
    ''', Color.Yellow))

    while True:
        line = input(cformat('> ', Color.Green))
        try:
            vm.eval(line)
        except Exception as e:
            eType = type(e)
            eName = eType.__name__
            if eType == SyntaxError:
                print(e.text)
                print((' ' * e.offset) + cformat('^', Color.Red))
            print(cformat(eName + ':', Color.Magenta), cformat(e, Color.Cyan))

except (KeyboardInterrupt, EOFError):
    exit(0)
finally:
    readline.write_history_file(history)

