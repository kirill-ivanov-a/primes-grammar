# primes-grammar

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
  -d, --derivation,  default=1
        "If 1 is passed, show derivation of the number in given grammar"
```
## Examples
