- [Lab 3: A simple lexer](#org5cfc323)
- [Theory](#org74327b2)
  - [Lexical analysis](#org732ae06)
  - [Ambiguous grammar](#org9117efa)
- [Objectives](#org5545cea)
- [Results](#org923194d)
- [Implementation](#orgc2bc5f8)




<a id="org5cfc323"></a>

# Lab 3: A simple lexer

Course
: Formal Languages &amp; Finite Automata

Author
: Balan Artiom


<a id="org74327b2"></a>

# Theory


<a id="org732ae06"></a>

## Lexical analysis

In English, words are composed of letters and words have meanings,
but the meaning isn&rsquo;t derived from the letters.
In fact, we don&rsquo;t even think of the letters when we read sentences,
we read the words as a whole and only care about their meaning.
That&rsquo;s kind of an analogy to the fact that parsers don&rsquo;t really care about the characters,
they care about syntactic units, called lexemes.

A lexeme is a string of characters that has a meaning.
Lexemes often correspond to terminals in a grammar (e.g. identifier, number, operator).

It&rsquo;s useful to store the location and length of each lexeme.
The data structure unit used to store lexemes together with information about them is called a token.


<a id="org9117efa"></a>

## Ambiguous grammar

Lexers for real programming languages often can&rsquo;t be constructed from the grammar alone,
since there are rules not captured in the grammar:

1.  The off-side rule (indentation-sensitive blocks) can&rsquo;t be described by context-free grammars
2.  Grammar rules can be ambiguous

When grammar rules are ambiguous, a string can be matched by multiple rules.
To counter this, for example ANTLR has disambiguating rules for tokenization ([docs](https://github.com/antlr/antlr4/blob/49b69bb31aa34654676a864b229a369680122470/doc/wildcard.md#nongreedy-lexer-subrules)):

-   Greedy and non-greedy regex lexer rules
-   Match the first rule occurring in the grammar

Ambiguous constructs should be used sparingly and in a strictly controlled fashion;
otherwise, there can be no guarantee as to what language is recognized by a parser (Aho, Alfred V and Sethi, Ravi and Ullman, Jeffrey D, 2007).

One quirk that proves disambiguization is complicated is the way ANTLR handles non-greedy rules (see rule 4 [in this section](https://github.com/antlr/antlr4/blob/49b69bb31aa34654676a864b229a369680122470/doc/wildcard.md#nongreedy-lexer-subrules)).

A token has a name and an optional value, which can be of any type (including `dict`).
Token names can correspond to nonterminals in the grammar,
but can also be groupings of terminals (e.g. &ldquo;operator&rdquo;).

Usually, whitespace doesn&rsquo;t make it past the lexer, but is still necessary to separate lexemes.
For example, `elsex` is an **idendtifier**, but `else x` is the keyword **else** and the **identifier** _x_.


<a id="org5545cea"></a>

# Objectives

-   [X] Implement a lexer and show how it works.


<a id="org923194d"></a>

# Results

I wrote a lexer for python-like syntax, hence, all the example strings are valid python code.

Let&rsquo;s parse a simple variable assignment:

```python
a_1 += 12 * 3 + 2
```

```text
/tmp/babel-P0bk7B/python-M2mdv0
```

Each token is represented by two things: a name and an optional value.
In this example, notice that the token for the variable `a` is of type `ID`,
which stands for &ldquo;identifier&rdquo;, and the token value is the name of the variable.

Similarly, numbers are represented by `NUMBER` tokens, with their value as the token value.

| Token name            | Token value |
|-----------------------|-------------|
| `TokenType.ID`        | `a_1`       |
| `TokenType.DELIMITER` | `+=`        |
| `TokenType.NUMBER`    | `12`        |
| `TokenType.OPERATOR`  | `*`         |
| `TokenType.NUMBER`    | `3`         |
| `TokenType.OPERATOR`  | `+`         |
| `TokenType.NUMBER`    | `2`         |
| `TokenType.EOF`       |             |

Now let&rsquo;s see how a lexer recognizes indentation:

```python
def t(arg):
    print(arg)
```

| Token name            | Token value |
|-----------------------|-------------|
| `TokenType.KEYWORD`   | `def`       |
| `TokenType.ID`        | `t`         |
| `TokenType.DELIMITER` | `(`         |
| `TokenType.ID`        | `arg`       |
| `TokenType.DELIMITER` | `)`         |
| `TokenType.DELIMITER` | `:`         |
| `TokenType.INDENT`    |             |
| `TokenType.ID`        | `print`     |
| `TokenType.DELIMITER` | `(`         |
| `TokenType.ID`        | `arg`       |
| `TokenType.DELIMITER` | `)`         |
| `TokenType.DEDENT`    |             |
| `TokenType.EOF`       |             |

Did you catch that?
The lexer generated two additional &ldquo;invisible&rdquo; tokens
to let the parser know about the indented block: `INDENT` and `DEDENT`.

You could visualize the token placement like this:

```text
1. def t(arg):
     v INDENT
2.    print(arg)
3.
  ^ DEDENT
```

Let&rsquo;s see a more complicated example:

```python
if a:
    if b:
        foo()
bar()
```

| Token name            | Token value |
|-----------------------|-------------|
| `TokenType.KEYWORD`   | `if`        |
| `TokenType.ID`        | `a`         |
| `TokenType.DELIMITER` | `:`         |
| `TokenType.INDENT`    |             |
| `TokenType.KEYWORD`   | `if`        |
| `TokenType.ID`        | `b`         |
| `TokenType.DELIMITER` | `:`         |
| `TokenType.INDENT`    |             |
| `TokenType.ID`        | `foo`       |
| `TokenType.DELIMITER` | `(`         |
| `TokenType.DELIMITER` | `)`         |
| `TokenType.DEDENT`    |             |
| `TokenType.DEDENT`    |             |
| `TokenType.ID`        | `bar`       |
| `TokenType.DELIMITER` | `(`         |
| `TokenType.DELIMITER` | `)`         |
| `TokenType.EOF`       |             |

Let&rsquo;s visualize this too:

```text
1. if a:
     v INDENT
2.    if b:
          v INDENT
3.         foo()
4. bar()
  ^ 2 x DEDENT
```

Notice how two `DEDENT` tokens were generated before `bar()`,
because we &ldquo;closed&rdquo; two indented blocks.

The lexer recognizes comments too and ignores them:

```python
 # this line has a bad indent
def t(arg):
    print(arg)  # this comment is inline
```

| Token name            | Token value |
|-----------------------|-------------|
| `TokenType.KEYWORD`   | `def`       |
| `TokenType.ID`        | `t`         |
| `TokenType.DELIMITER` | `(`         |
| `TokenType.ID`        | `arg`       |
| `TokenType.DELIMITER` | `)`         |
| `TokenType.DELIMITER` | `:`         |
| `TokenType.INDENT`    |             |
| `TokenType.ID`        | `print`     |
| `TokenType.DELIMITER` | `(`         |
| `TokenType.ID`        | `arg`       |
| `TokenType.DELIMITER` | `)`         |
| `TokenType.DEDENT`    |             |
| `TokenType.EOF`       |             |

Notice that the first line has a bad indent (first line can&rsquo;t be indented in python),
but since it&rsquo;s a comment, we can ignore this issue (one more edge-case to consider).

There&rsquo;s one type of indentation error that can be recognized by the lexer (and 3 others that can only be recognized by the parser),
and that&rsquo;s the &ldquo;inconsistent dedent&rdquo;:

```python
def foo(a):
    if a == 1:
        return 1
   return 0
```

The lexer simply raises an exception for this example.

Notice how some delimiters start like operators, and viceversa:

```python
a += b == c
```

| Token name            | Token value |
|-----------------------|-------------|
| `TokenType.ID`        | `a`         |
| `TokenType.DELIMITER` | `+=`        |
| `TokenType.ID`        | `b`         |
| `TokenType.OPERATOR`  | `==`        |
| `TokenType.ID`        | `c`         |
| `TokenType.EOF`       |             |

In this case, the operator `==` starts like the delimiter `=`, and the delimiter `+=` starts like the operator `+`.
I&rsquo;m not sure what&rsquo;s the proper way to deal with this, so my code is a bit hacky.


<a id="orgc2bc5f8"></a>

# Implementation

Indentation handling is implemented as described in the [python docs](https://docs.python.org/3/reference/lexical_analysis.html#indentation).

The entire &ldquo;lexer&rdquo; is a single function `get_tokens(s) -> ls`
that takes a string to be tokenized, and returns a list of all the tokens.

Initially I tried wrapping the tokenizer inside a class, but it didn&rsquo;t make sense
and only made things more obscure and complicated.
I don&rsquo;t see why you would need to maintain the state of a lexer by reading tokens one by one,
when you could instead get all the tokens at once.
And if you don&rsquo;t need a state, there&rsquo;s no need for an object.

The `get_tokens` function reads characters using either `getch()`  or `peek()`,
depending on whether it wants to also consume the character.

The entire function is a loop that tokenizes the entire string,
until there&rsquo;s no more characters left, after which it generates the last token, `EOF`.

