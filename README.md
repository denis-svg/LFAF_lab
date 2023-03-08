
# Table of Contents

1.  [Implementation of formal languages](#org23fc264)
2.  [Objectives](#orgf67a9af)
    1.  [Lab 1](#orgc61ecd0)
    2.  [Lab 2](#orgb81e659)
        1.  [Results](#org58bd15e)
            1.  [Convert NFA to Grammar](#org825f575)
            2.  [Find out if FA is nondeterministic](#org4b9ed35)
            3.  [Convert NFA to DFA](#org58ce45f)
            4.  [Visualize the finite automatons](#orga324ea2)
3.  [Implementation](#org2a1dfbc)
4.  [Theory](#org07ac556)



<a id="org23fc264"></a>

# Implementation of formal languages

-   **Course:** Formal Languages & Finite Automata
-   **Author:** Balan Artiom


<a id="orgf67a9af"></a>

# Objectives


<a id="orgc61ecd0"></a>

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


<a id="orgb81e659"></a>

## Lab 2

-   [X] Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.
-   [X] Implement conversion of a finite automaton to a regular grammar.
-   [X] Determine whether your FA is deterministic or non-deterministic.
-   [X] Implement some functionality that would convert an NDFA to a DFA.
-   [X] Represent the finite automaton graphically (Optional, and can be considered as a bonus point):
-   [X] Document everything in the README
-   [ ] Test string validation with the new more general DFA


<a id="org58bd15e"></a>

### Results

Here&rsquo;s the NFA I got:

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

I can convert it to an NFA, and then do many things with it.

    nfa = NFA(S=S, A=A, s0=s0, d=d, F=F)


<a id="org825f575"></a>

#### Convert NFA to Grammar

I can find out the type of the resulting grammar in the Chomsky hierarchy:
Or print out the grammar if I format it a bit:

    for l,r in g.P.items():
        print(''.join(l), '->', ' | '.join([' '.join(t) for t in r]))

    q0 -> a q1
    q1 -> b q1 | a q2
    q2 -> b q3 | b q2
    q3 -> b q4 | a q1
    q4 ->


<a id="org4b9ed35"></a>

#### Find out if FA is nondeterministic

Even though it&rsquo;s an NFA, it could be that it doesn&rsquo;t have nondeterministic transitions.
We can find that out:

    print(nfa.is_deterministic())

    False


<a id="org58ce45f"></a>

#### Convert NFA to DFA

    dfa = nfa.to_DFA()
    print(dfa)

    {frozenset({'q2', 'q3'}), frozenset({'q1'}), frozenset({'q2', 'q4', 'q3'}), frozenset({'q0'}), frozenset({'q2'})}, {'a', 'b'}, {'q0'}, {(frozenset({'q0'}), 'a'): {'q1'}, (frozenset({'q1'}), 'a'): {'q2'}, (frozenset({'q1'}), 'b'): {'q1'}, (frozenset({'q2'}), 'b'): {'q2', 'q3'}, (frozenset({'q2', 'q3'}), 'a'): {'q1'}, (frozenset({'q2', 'q3'}), 'b'): {'q2', 'q4', 'q3'}, (frozenset({'q2', 'q4', 'q3'}), 'a'): {'q1'}, (frozenset({'q2', 'q4', 'q3'}), 'b'): {'q2', 'q4', 'q3'}}, {frozenset({'q2', 'q4', 'q3'})}

Now that we have a DFA, we can easily validate some strings according to the grammar.
But first, let&rsquo;s generate a few:

    l = [g.constr_word() for _ in range(5)]
    print(l)

    ['aabababb', 'aabababbb', 'aababbbbabb', 'abbbabb', 'aabbbbbbbababbbbbb']

Let&rsquo;s verify that they&rsquo;re all valid:

    print(all(dfa.verify(w) for w in l))

    True


<a id="orga324ea2"></a>

#### Visualize the finite automatons

Here&rsquo;s the NFA:

    fn = nfa.draw('./img', 'variant_3_nfa')
    print(fn)

![img](img/variant_3_nfa.gv.svg)

And the DFA:

    fn = dfa.draw('./img', 'variant_3_dfa')
    print(fn)

![img](img/variant_3_dfa.gv.svg)


<a id="org2a1dfbc"></a>

# Implementation

I wrote very extensive comments inside source code files, so refer to those please.


<a id="org07ac556"></a>

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

