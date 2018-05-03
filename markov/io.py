#!/usr/bin/env python3

import os
import sys
import re


class Input:
    """
    Class for optimizing the input for files.
    Also provides unified interface for directory and stdin input.
    """

    def __init__(self, input_dir):
        self._input_dir = input_dir

    def files(self):
        """
        Main method of class - returns iterable of files.
        :return: iterable with opened files
        """
        return self.__files_generator() if self._input_dir else (sys.stdin,)

    def __files_generator(self):
        """
        Returns names of all files in directory recursively
        :return: yields file names
        """
        tree = os.walk(self._input_dir)
        for directory, _, file_list in tree:
            for file in file_list:
                with open(os.path.join(directory, file), "r") as f:
                    yield f

    @staticmethod
    def prepare_symbols(text):
        """
        Removes all unwanted symbols from text
        :param text: text with unwanted symbols
        :return: filtered text
        """
        text = re.sub(r"([{}])+".format(Output.symbols),
                      r" \1",
                      text)
        text = re.sub(r"[{}]+".format("\"#$%()*+/<=>@[\\]^_{|}~\n"),
                      r"",
                      text)
        text = re.sub(r"\s+", " ", text)
        return text


class Output:
    symbols = r".,!?&:;"

    @staticmethod
    def print(words):
        """
        Processes a word list and prints the text.
        :param words: Iterable with words
        :return: None
        """
        text = " ".join(words)
        text = re.sub(r" ([{}])+".format(Output.symbols),
                      r"\1",
                      text)
        print(text.capitalize())
