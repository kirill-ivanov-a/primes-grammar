# primes-grammar
![workflow](https://github.com/kirill-ivanov-a/primes-grammar/actions/workflows/code_style.yml/badge.svg)

## About
Yet another machine to grammar converter. The following transformations are available:
 - from LBA to CSG;
 - from TM to T0-grammar.

Prime grammars are located [here](https://github.com/kirill-ivanov-a/primes-grammar/tree/main/resources).

## Requirements

Python >=3.8. No external libraries were used.

## Installation
1. Clone this repository:
```bash
git clone https://github.com/kirill-ivanov-a/primes-grammar.git
```
2. Go to source directory:
```bash
cd primes-grammar/
```
## Usage
__NOTE:__ symbol `$` is used as epsilon in T0 grammar

```bash
usage: python -m src <args>

arguments:
  -n, --number
        "Decimal number for primality check"

optional arguments:
  -h, --help
        "Show help message and exit"
  -g, --grammar,  default=t0
        "Choose grammar (t0 | t1) for primality check"
  -d, --derivation,  default=0
        "If 1 is passed, show derivation of the number in given grammar"
```
## Examples

```bash
python3 -m src --number=2 --grammar=t0 --derivation=1

INFO: 2 is prime
Start symbol: S
Used production: S -> S28 S23 S27
Sentence: S28 S23 S27
Used production: S28 -> $
Sentence: $ S23 S27
Used production: S27 -> S24 S27
Sentence: $ S23 S24 S27
Used production: S23 S24 -> S4 S19
Sentence: $ S4 S19 S27
Used production: S27 -> S24 S27
Sentence: $ S4 S19 S24 S27
Used production: S19 S24 -> S4 S10
Sentence: $ S4 S4 S10 S27
Used production: S27 -> S6
Sentence: $ S4 S4 S10 S6
Used production: S6 -> S3
Sentence: $ S4 S4 S10 S3
Used production: S10 S3 -> S11 S3
Sentence: $ S4 S4 S11 S3
Used production: S11 S3 -> S11 $ S11
Sentence: $ S4 S4 S11 $ S11
Used production: S11 -> $
Sentence: $ S4 S4 S11 $ $
Used production: S4 S11 -> S11 1 S11
Sentence: $ S4 S11 1 S11 $ $
Used production: S11 -> $
Sentence: $ S4 S11 1 $ $ $
Used production: S4 S11 -> S11 1 S11
Sentence: $ S11 1 S11 1 $ $ $
Used production: S11 -> $
Sentence: $ $ 1 S11 1 $ $ $
Used production: S11 -> $
Sentence: $ $ 1 $ 1 $ $ $
```

```bash
python3 -m src --number=11 --grammar=t1 --derivation=0

INFO: 11 is prime
```

```bash
python3 -m src --number=6 --grammar=t0 --derivation=0

INFO: 6 is not prime
```
