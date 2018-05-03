#!/usr/bin/env python3

import json
import random
import collections
import markov.io


class Model:
    """
    Contains all logic for creating sequences of words.
    """

    def __init__(self):
        self._data = collections.defaultdict(
            lambda: collections.defaultdict(lambda: 0))

    def load(self, json_string):
        """
        Loads model from string.
        :param json_string: Json string with model contents
        :return: None
        """
        self._data.update(json.loads(json_string))

    def save(self, file):
        """
        Saves model to the file.
        :param file: file, where model will be saved
        :return: None
        """
        json.dump(self._data, file,
                  sort_keys=True,
                  indent=1,
                  ensure_ascii=False)

    def __add_connection(self, pair):
        """
        Adds (updates) connection between two words in model structure.
        :param pair: Words to be connected
        :return: None
        """
        self._data[pair[0]][pair[1]] += 1

    def __get_next_word(self, current_word):
        """
        Returns next word of sequence based on word weights and last word.
        :param current_word: Last generated word
        :return: The new word
        """
        words = tuple(self._data[current_word].keys())
        if not words:
            return random.choice(tuple(self._data.keys()))
        weights = tuple(self._data[current_word].values())
        return random.choices(words, weights=weights)[0]

    def process(self, io: markov.io.Input, make_lowercase):
        """
        Updates current model with contents of given markov.io.Input object
        :param io: content that will be added to the model
        :param make_lowercase: True if all words should be converted to
        lowercase, False otherwise
        :return: None
        """
        for file in io.files():
            last_word = None
            for string in file:
                if "decode" in dir(string):
                    string = string.decode()
                string = markov.io.Input.prepare_symbols(string)
                if make_lowercase:
                    string = string.lower()

                if string.isspace() or not string:
                    continue

                words = string.split()
                if last_word:
                    words = [last_word] + words
                last_word = words[-1]
                for word1, word2 in self.iterate_over_pairs(string.split()):
                    self.__add_connection((word1, word2))

    @staticmethod
    def iterate_over_pairs(words: list):
        """
        Iterates over pairs of words
        :param words: List of words to be iterated over
        :return: The new iterable of pairs
        """
        return zip(words[:-1], words[1:])

    def get_random_sequence(self, length, first_word=None):
        """
        Generates random sequence of words of given length.
        :param length: Length of sequence
        :param first_word: First word or None
        :return: Yields next word
        """
        current = first_word or random.choice(list(self._data.keys()))
        for i in range(length):
            yield current
            current = self.__get_next_word(current)
