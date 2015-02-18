#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import vm
import code

if __name__ == '__main__':

    vm = vm.VM()

    try:
        while True:
            s = input('>>> ')
            vm.eval(s)
    except (KeyboardInterrupt, EOFError):
        exit(0)

