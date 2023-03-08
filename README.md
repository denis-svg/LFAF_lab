
# Table of Contents

1.  [Implementation of formal languages](#orga85c043)
2.  [Objectives](#org98ba3df)
    1.  [Lab 1](#org36c819b)
    2.  [Lab 2](#orgf24bf14)
        1.  [Convert NFA to Grammar](#orge9b501e)
        2.  [Find out if FA is nondeterministic](#orgd72b554)
        3.  [Convert NFA to DFA](#orgf24bf66)
        4.  [Visualize the finite automatons](#org2888e42)
3.  [Implementation](#org2ecb4e3)
4.  [Theory](#org1d264fe)



<a id="orga85c043"></a>

# Implementation of formal languages

-   **Course:** Formal Languages & Finite Automata
-   **Author:** Balan Artiom


<a id="org98ba3df"></a>

# Objectives


<a id="org36c819b"></a>

## Lab 1

-   [X] Implement a  `Grammar` and a `FiniteAutomaton`, with the respective methods:
    -   `Grammar`
        -   `generateString()`
        -   `convert_to_FSM()`
    -   `FiniteAutomaton`
        -   `check_string()`
-   [X] Showcase the code:
    -   generate 5 words with the grammar
    -   create a FSM from the grammar
    -   check that the generated words are valid according to the FSM


<a id="orgf24bf14"></a>

## Lab 2

-   [X] Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.
-   [X] Implement conversion of a finite automaton to a regular grammar.
-   [X] Determine whether your FA is deterministic or non-deterministic.
-   [X] Implement some functionality that would convert an NDFA to a DFA.
-   [X] Represent the finite automaton graphically (Optional, and can be considered as a bonus point):
-   [X] Document everything in the README
-   [ ] Test string validation with the new more general DFA

Here's the NFA I got:

    Q = {q0,q1,q2,q3,q4},
    ∑ = {a,b},
    F = {q4},
    δ(q0,a) = q1,
    δ(q1,b) = q1,
    δ(q1,a) = q2,
    δ(q2,b) = q2,
    δ(q2,b) = q3,
    δ(q3,b) = q4,
    δ(q3,a) = q1.

After manually rewriting it like this:

    S = {"q0","q1","q2","q3","q4"}
    A = {"a","b"}
    s0 = "q0"
    F = {"q4"}
    d = {("q0","a"): {"q1"},
         ("q1","b"): {"q1"},
         ("q1","a"): {"q2"},
         ("q2","b"): {"q2", "q3"},
         ("q3","b"): {"q4"},
         ("q3","a"): {"q1"}}

I can initialize an NFA, and then do many things with it.

    nfa = NFA(S=S, A=A, s0=s0, d=d, F=F)


<a id="orge9b501e"></a>

### Convert NFA to Grammar

I can find out the type of the resulting grammar in the Chomsky hierarchy:
Or print out the grammar if I format it a bit:

    for l,r in g.P.items():
        print(''.join(l), '->', ' | '.join([' '.join(t) for t in r]))

    q0 -> a q1
    q1 -> b q1 | a q2
    q2 -> b q2 | b q3
    q3 -> b q4 | a q1
    q4 ->


<a id="orgd72b554"></a>

### Find out if FA is nondeterministic

Even though it's an NFA, it could be that it doesn't have nondeterministic transitions.
We can find that out:

    print(nfa.is_deterministic())

    False


<a id="orgf24bf66"></a>

### Convert NFA to DFA

    dfa = nfa.to_DFA()
    print(dfa)

    {frozenset({'q3', 'q2'}), frozenset({'q3', 'q4', 'q2'}), frozenset({'q0'}), frozenset({'q2'}), frozenset({'q1'})}, {'a', 'b'}, {'q0'}, {(frozenset({'q0'}), 'a'): {'q1'}, (frozenset({'q1'}), 'a'): {'q2'}, (frozenset({'q1'}), 'b'): {'q1'}, (frozenset({'q2'}), 'b'): {'q3', 'q2'}, (frozenset({'q3', 'q2'}), 'a'): {'q1'}, (frozenset({'q3', 'q2'}), 'b'): {'q3', 'q4', 'q2'}, (frozenset({'q3', 'q4', 'q2'}), 'a'): {'q1'}, (frozenset({'q3', 'q4', 'q2'}), 'b'): {'q3', 'q4', 'q2'}}, {frozenset({'q3', 'q4', 'q2'})}

Now that we have a DFA, we can easily validate some strings according to the grammar.
But first, let's generate a few:

    l = [g.constr_word() for _ in range(5)]
    print(l)

    ['aabbaabababaababbabababbbbbbaabababababb', 'abbbbabbbabbabb', 'abbbbabbbbbaababbababbababbbabbb', 'abbabbbb', 'aabbbbbbbbb']

Let's verify that they're all valid:

    print(all(dfa.verify(w) for w in l))

    True


<a id="org2888e42"></a>

### Visualize the finite automatons

Here's the NFA:

    fn = nfa.draw('./img', 'variant_3_nfa')
    print(fn)

![img](img/variant_3_nfa.gv.svg)

And the DFA:

    fn = dfa.draw('./img', 'variant_3_dfa')
    print(fn)

![img](img/variant_3_dfa.gv.svg)


<a id="org2ecb4e3"></a>

# Implementation

I wrote very extensive comments inside source code files, so refer to those please.


<a id="org1d264fe"></a>

# Theory

An instance of a **formal language** is a set of *words* which are composed of *letters*.
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

