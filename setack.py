#!/usr/bin/env python3

import sys
import os

import repl
from vm import VM


if __name__ == '__main__':
    if len(sys.argv) == 1:
        repl.run()
        sys.exit(0)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)
    else:
        vm = VM()
        vm.evalFile(filepath)
