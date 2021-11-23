# primes-grammar
![workflow](https://github.com/kirill-ivanov-a/primes-grammar/actions/workflows/code_style.yml/badge.svg)

## About
Yet another machine to grammar converter. The following transformations are available:
 - from LBA to CSG;
 - from TM to T0-grammar.

Prime grammars are located [here](https://github.com/kirill-ivanov-a/primes-grammar/tree/main/resources).

## Requirements

Python >=3.8. No external libraries were used.

## Usage

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
python3 -m src --number=2 --grammar=t1 --derivation=1

INFO: 2 is prime
Start symbol: S55
Used production: S55 -> S1 S27
Sentence: S1 S27
Used production: S1 -> S24
Sentence: S24 S27
Used production: S27 -> S60
Sentence: S24 S60
Used production: S24 S60 -> S145 S57
Sentence: S145 S57
Used production: S57 -> S86
Sentence: S145 S86
Used production: S86 -> S59
Sentence: S145 S59
Used production: S59 -> 1
Sentence: S145 1
Used production: S145 1 -> 1 1
Sentence: 1 1
```

```bash
python3 -m src --number=6 --grammar=t0 --derivation=1

INFO: 6 is not prime
```
