#!/usr/bin/env python3

import argparse
import markov
import os.path


def main(args):
    model = markov.model.Model()

    files = markov.input.Input(args.input_dir)
    for contents in files.read_strings():
        model.process(contents, args.lc)

    print(model._data)

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
