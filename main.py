#!/usr/bin/env python3
from icecream import ic

from src.grammar import *
from src.automata import *


if __name__ == '__main__':
    # Variant #3 NFA
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

    nfa = NFA(S=S, A=A, s0=s0, d=d, F=F)
    g = nfa.to_grammar()
    ic(g)
    ic(g.type())
    ic(nfa)
    dfa = nfa.to_DFA()
    ic(dfa)

    w = g.constr_word()
    ic(w)


    # nfa.draw('./img', 'variant_3_nfa')
    # fn = dfa.draw('./img', 'variant_3_dfa')
