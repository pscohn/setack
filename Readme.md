Forth inspired language to operate on sets

__Todo__
* Lex and parse rest of built-in operations and sets
* Implement interpreter in python and then rpython?

__Semantics of Setack__

__Grammar__

```js
statement  = expresssion { whitespace statement }
expression = set
           | pair
           | boolean
           | number
           | symbol
```

__Built-ins__

| symbol | description |
| ------ | ----------- |
| ∅ | Empty set |
| ℕ | Natural numbers |
| ℝ | Real numbers |
| ∈ | membership |
| ∉ | membership |
| ⊆ | subset |
| ∪ | union |
| ∩ | intersection |
| \ | difference |
| ∆ | symmetric difference |
| x | cartesian product |
| ℙ | power set |

