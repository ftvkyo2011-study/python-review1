#!/usr/bin/env python3

import json
import random
import re
import string


class Model:
    def __init__(self):
        self._data = dict()

    def load(self, json_string):
        self._data.update(json.loads(json_string))

    def save(self, file):
        file.write(json.dumps(self._data, sort_keys=True, indent=4))

    def add_connection(self, pair):
        d = self._data
        left, right = pair

        if left in d:
            if right in d[left].keys():
                d[left][right] += 1
            else:
                d[left][right] = 1
        else:
            d[left] = {right: 1}

    def get_next_word(self, current_word):
        # TODO: weighted choice
        return random.choice(list(self._data[current_word].keys()))

    def process(self, text, make_lowercase):
        if "decode" in dir(text):
            text = text.decode()
        text = Model.remove_punctuation_and_spaces(text)
        if make_lowercase:
            text = text.lower()
        for w1, w2 in Model.iterate_over_pairs(text.split()):
            self.add_connection((w1, w2))

    @staticmethod
    def iterate_over_pairs(words: list):
        return zip(words[:-1], words[1:])

    @staticmethod
    def remove_punctuation_and_spaces(text):
        punctuation = re.sub(r"[-'&$@#`]+", "", string.punctuation)
        line = re.sub(r"[{}]+".format(punctuation), " ", text)
        line = re.sub(r"\s+", " ", line)
        return line

    def get_random_sequence(self, length, first_word=None):
        current = first_word if first_word else random.choice(list(self._data.keys()))
        for i in range(length):
            yield current
            current = self.get_next_word(current)
