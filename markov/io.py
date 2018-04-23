#!/usr/bin/env python3

import os
import sys
import re


class Input:
    def __init__(self, input_dir):
        self._input_dir = input_dir

    def files(self):
        return self.__files_generator() if self._input_dir else (sys.stdin,)

    def __files_generator(self):
        tree = os.walk(self._input_dir)
        for directory, _, file_list in tree:
            for file in file_list:
                with open(os.path.join(directory, file), "r") as f:
                    yield f

    @staticmethod
    def filter_symbols(text):
        text = re.sub(r"[{}]+".format("!\"#$%&()*+,./:;<=>?@[\]^_{|}~\n"),
                      "",
                      text)
        text = re.sub(r"\s+", " ", text)
        return text
