#!/usr/bin/env python3

import json
import random
import collections
import markov.io


class Model:
    def __init__(self):
        self._data = collections.defaultdict(
            lambda: collections.defaultdict(lambda: 0))

    def load(self, json_string):
        self._data.update(json.loads(json_string))

    def save(self, file):
        file.write(json.dumps(self._data, sort_keys=True, indent=4))

    def __add_connection(self, pair):
        d = self._data
        left, right = pair
        d[left][right] += 1

    def __get_next_word(self, current_word):
        # TODO: weighted choice
        return random.choice(list(self._data[current_word].keys()))

    def process(self, io: markov.io.Input, make_lowercase):
        for file in io.files():
            last_word = None
            for s in file:
                if "decode" in dir(s):
                    s = s.decode()
                s = markov.io.Input.filter_symbols(s)
                if make_lowercase:
                    s = s.lower()

                if s.isspace() or not s:
                    continue

                words = s.split()
                if last_word:
                    words = [last_word] + words
                last_word = words[-1]
                for w1, w2 in self.iterate_over_pairs(s.split()):
                    self.__add_connection((w1, w2))

    @staticmethod
    def iterate_over_pairs(words: list):
        return zip(words[:-1], words[1:])

    def get_random_sequence(self, length, first_word=None):
        current = first_word or random.choice(list(self._data.keys()))
        for i in range(length):
            yield current
            current = self.__get_next_word(current)
