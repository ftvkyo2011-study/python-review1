#!/usr/bin/env python3

import argparse
import markov


def main(args):
    """
    Secondary function of text generator - collects data into model.
    Works with model file aka args.model or with standard input.
    :param args: argparse result. Should contain "model", "input_dir" and "lc".
    :return: None
    """
    model = markov.model.Model()
    io = markov.io.Input(args.input_dir)

    model.process(io, args.lc)

    with open(args.model, "w") as output_file:
        model.save(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model",
                        default="model.json",
                        help="Path to model file")
    parser.add_argument("--input-dir",
                        default=None,
                        help="Directory with input files (stdin if None)")
    parser.add_argument("--lc",
                        action="store_true",
                        help="Force lowercase")
    namespace = parser.parse_args()

    main(namespace)
