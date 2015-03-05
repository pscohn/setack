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

Setack is an interpreted, dynamically-typed, stack-oriented programming language to operate on sets.

The repl comes with:
   * auto-complete
   * history
   * syntax and type errors
   * built-in set operations
   * documentation to help you learn about set operations
   
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

__Todo__
* implement define-function
* add control flow
