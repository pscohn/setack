Forth inspired language to operate on sets

__Todo__
* Lex and parse rest of built-in operations and sets
* Implement interpreter in python and then rpython?

__Semantics of Setack__

__Grammar__

statement  = expresssion { whitespace statement }
expression = set
           | pair
           | boolean
           | number
           | symbol

(* -------------------------------- *)

__Built-in sets__ 
* Empty set
* Natural numbers
* Real numbers

__Built-in relations__
* membership              (∈):
* not-member              (∉):

__Build-in operations__
* subset                  (⊆): A ⊆ B means every element of A is also an element of B
* union                   (∪): A ∪ B means the set of those elements which are either in A, or in B, or in both.
* intersection            (∩): A ∩ B means the set that contains all those elements that A and B have in common.
* difference              (\): In the left set and not in the right set
* (symmetric difference    (∆, symmetric difference): In either set but not in both
* (x, cartesian product):
* (ℙ, power set)

