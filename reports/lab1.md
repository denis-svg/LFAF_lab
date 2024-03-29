- [Implementation of formal languages](#orgb1ff54f)
- [Theory](#org030647e)
- [Objectives](#org2544032)
- [Implementation](#org0bd294b)
  - [Deterministic or not?](#org0bffcc3)




<a id="orgb1ff54f"></a>

# Implementation of formal languages

Course
: Formal Languages &amp; Finite Automata

Author
: Balan Artiom


<a id="org030647e"></a>

# Theory

An instance of a **formal language** is a set of _words_ which are composed of _letters_.
The set of words can be defined in many ways:

-   by simply enumerating all the valid elements (words)
-   by defining an alphabet and a grammar

An **alphabet** is a set of letters.

A **grammar** is a set of rules that define how to form valid words from the alphabet.

A regular grammar is one in which all production rules in P are of one of the following forms:

-   A → a
-   A → aB
-   A → ε

where A, B, S ∈ N are non-terminal symbols, a ∈ Σ is a terminal symbol,
and ε denotes the empty string, i.e. the string of length 0. S is called the start symbol.


<a id="org2544032"></a>

# Objectives

Implement a  `Grammar` and a `FiniteAutomaton`, with the respective methods:

-   `Grammar`
    -   `generateString()`
    -   `convert_to_FSM()`
-   `FiniteAutomaton`
    -   `check_string()`

Showcase the code:

-   generate 5 words with the grammar
-   create a FSM from the grammar
-   check that the generated words are valid according to the FSM


<a id="org0bd294b"></a>

# Implementation

To construct words with the grammar,
I simply picked a random rule from the list for each non-terminal and built the word until it hit a terminal symbol.

```python
def constr_word(self):
    from random import choice
    w = self.S
    while w[-1] in self.VN:
        # There's a slight probability this will go on for too long
        N = w[-1]
        w = w[:-1] + choice(self.P[N])
    return w
```

To convert the grammar to an FSM,
I create a dictionary that maps each pair `(state, letter)` to the next state `(new_state)`.

```python
def to_FSM(self):
    fin_state = "End"
    d = {}
    for s0, rl in self.P.items():
        d |= {(s0, r[0]): r[1] if len(r) == 2 else fin_state for r in rl}
    return FSM(self.VN | {fin_state}, self.S, d, {fin_state})
```

Verifying a word is done by going through each letter
and doing the transition from the current state according to the rule from the dictionary of transitions.
If there isn&rsquo;t such a transition, the word is not valid.
If in the end the current state is not a final state, the word is not valid.

```python
def verify(self, w):
    s = self.s0
    for l in w:
        ns = self.d.get((s, l))
        if not ns:
            return False
        s = ns
    return s in self.F
```


<a id="org0bffcc3"></a>

## Deterministic or not?

Variant #3 defines a non-deterministic language, but not #2 for example.
I&rsquo;m not sure if this was intended,
but to bring justice I picked #2 even though I&rsquo;m 3rd on the list.

