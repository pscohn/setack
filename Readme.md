Forth inspired language to operate on sets

__Todo__
* Implement interpreter in python and then rpython?

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

| Symbol | Description |
| :----- | :---------- |
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

