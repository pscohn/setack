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

__Data Types__
* Set
* Tuple
* Boolean
* Integer
* Float
* Symbol

__Grammar__
```hs
expr  = bool
      | int
      | float
      | symbol
      | set
      | tuple
set   = "{" expr {, expr} "}"
tuple = "(" expr {, expr} ")"
```

__ToDo__
* Iron out bugs with lexical stack evaluation
* Implement (man|doc) command to give wikipedia answer about set command
* Help command, type command, () type => tuple
* Implement procedures: map from variable to setexp, need a setexp literal
  symbol (symbol*) [body] proc
  x (x, y) [x y +]
  [] = set expression literal
