#!/usr/bin/env python3

import argparse
import markov


def main(args):
    """
    Main function of text generator - generates sequences of words from model.
    Works with model aka args.model.
    :param args: argparse result. Should contain "model", "seed", "length" and
    "output"
    :return: None
    """
    model = markov.model.Model()

    with open(args.model) as input_file:
        model.load(input_file.read())

    markov.io.Output.print(model.get_random_sequence(args.length, args.seed))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model",
                        default="model.json",
                        help="Path to model file")
    parser.add_argument("--seed",
                        default=None,
                        help="First word of sequence (random if None)")
    parser.add_argument("--length",
                        help="Sequence length",
                        type=int,
                        required=True)
    parser.add_argument("--output",
                        default=None,
                        help="Output file (stdout if None)")
    namespace = parser.parse_args()

    main(namespace)
