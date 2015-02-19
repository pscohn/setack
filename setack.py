#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import readline
import vm

from colorprint import *

vm = vm.VM()

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

