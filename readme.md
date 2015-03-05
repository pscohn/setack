```
   (                                )
   )\ )     *   )   (       (    ( /(
  (()/((  ` )  /(   )\      )\   )\())
   /(_))\  ( )(_)|(((_)(  (((_)|((_)\
  (_))((_)(_(_()) )\ _ )\ )\___|_ ((_)
  / __| __|_   _| (_)_\(_|(/ __| |/ /
  \__ \ _|  | |    / _ \  | (__  ' <
  |___/___| |_|   /_/ \_\  \___|_|\_\

stack-oriented language to operate on sets
```

Setack is an interpreted, dynamically-typed, stack-oriented programming language to operate on sets. Whew!

The repl comes with auto-complete, history, beautiful syntax and type errors, a variety of built-ins to help you expore the stack and environment, and documentation to help you learn about set operations.

__Grammar__
```
expr  = atom { " " expr }
      | atom
atom  = set
      | tuple
      | bool
      | float
      | int
      | string
      | symbol
set   = "{" expr { "," expr } "}"
tuple = "(" expr { "," expr } ")"
thunk = "[" expr { "," expr } "]"
```

__Todo__
* define-function
* control-flow

__Presentation__

* REPL
    Auto-complete > <tab>
    Show documentation > help
    Syntax errors > {1,
    Type errors   > {1} 2 union

* Builtins
    union
    intersection
    difference
    symmetric-difference
    cartesian-product
    power-set
    in
    not-in
    subset
    proper-subset

* Show language feature
    > define-symbol
    > stack sub-expressions

* Run goodbye-world.setack
