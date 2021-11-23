import argparse
import sys

from src.checker import check_prime


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--grammar",
        "-g",
        help="Type of grammar ('t0' | 't1'), default='t0'",
        default="t0",
    )
    parser.add_argument(
        "--number", "-n", help="Decimal number for primality test", required=True
    )
    parser.add_argument(
        "--derivation",
        "-d",
        help="Show derivation path ('1' | '0'), default=0",
        default=0,
    )

    args = parser.parse_args(args=argv)

    if args.grammar not in ("t0", "t1"):
        raise argparse.ArgumentTypeError(
            "Invalid type of grammar: Possible types are 't0' or 't1'"
        )
    if not args.number.isdecimal():
        raise argparse.ArgumentTypeError(
            "Invalid number: Number should be any decimal number"
        )
    if args.derivation not in ("0", "1"):
        raise argparse.ArgumentTypeError(
            "Invalid derivation value: Possible options are '0' or '1'"
        )

    return check_prime(
        grammar_type=args.grammar, number=args.number, derivation=args.derivation
    )


if __name__ == "__main__":
    main(sys.argv[1:])
