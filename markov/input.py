#!/usr/bin/env python3

import os
import sys


class Input:
    def __init__(self, input_dir):
        self._strings = []
        if input_dir:
            self._strings.extend(Input.load_files_gen(input_dir))
        else:
            self._strings.append(sys.stdin.read())

    @staticmethod
    def load_files_gen(input_dir):
        tree = os.walk(input_dir)
        for directory, _, file_list in tree:
            for file in file_list:
                with open(os.path.join(directory, file), "r") as f:
                    contents = f.read()
                yield contents

    def read_strings(self):
        return (x for x in self._strings)
