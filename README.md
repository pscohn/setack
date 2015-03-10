```
   (                                )
   )\ )     *   )   (       (    ( /(
  (()/((  ` )  /(   )\      )\   )\())
   /(_))\  ( )(_)|(((_)(  (((_)|((_)\
  (_))((_)(_(_()) )\ _ )\ )\___|_ ((_)
  / __| __|_   _| (_)_\(_|(/ __| |/ /
  \__ \ _|  | |    / _ \  | (__  ' <
  |___/___| |_|   /_/ \_\  \___|_|\_\
```

Setack is:
   * a domain specific language for operating on sets
   * stack-oriented   
   * interpreted
   * dynamically-typed

The repl comes with:
   * auto-complete
   * history
   * syntax and type errors
   * built-in set operations
   * documentation to help you learn about set operations

__Built-in Functions__
   * help
   * print
   * show-stack
   * show-symbols
   * define-symbol
   * define-proc
   * run-file
   * eval-thunk
   * if

__Built-in Set Operations__
   * union
   * intersection
   * difference
   * symmetric-difference
   * cartesian-product
   * power-set
   * in
   * not-in
   * subset
   * proper-subset

__Built-in Number Operations__
   * multiply
   * divide
   * add
   * subtract

__Grammar__
```js
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
