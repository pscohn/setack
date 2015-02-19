#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import readline
import vm

from colorprint import *

history = '{}/{}'.format(os.path.expanduser('~'), '.setack_history')
vm = vm.VM()

if not os.path.exists(history):
    open(history, 'w')

readline.read_history_file(history)

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

