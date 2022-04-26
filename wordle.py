import os
import re


def check_for_prime(n):
    """ check for a prime number """
    
    
    
    

class Wordle():
    """ Object for finding wordle solutions using regex with a simple interface """

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), './answers.txt')) as f:
            self._words = f.read().splitlines()

        self._filter_green = r""
        self._filter_yellow = r""
        self._yellow = ""
        self._yellow_pos_filters = []
        self._grey = ""
        self._grey_filters = []

    def __call__(self):
        self.words()

    def get_num_repeat_chars(self, word):
        """ return the number of repeat characters in a word """
        return len(re.findall(r"(.)\1+", word))

    def get_soft_filters(self, search):
        unique_search = "".join(set(search))
        return [rf"(?=.*{char})" for char in unique_search]

    def filter_yellow(self, word):
        self._filter_yellow = "".join(self.get_soft_filters(self._yellow))

        for pos_filter in self._yellow_pos_filters:
            match = re.match(pos_filter, word)
            if not match:
                return match

        return re.match(self._filter_yellow, word)

    def filter_green(self, word):
        """ returns the green filter """
        return re.match(self._filter_green, word)

    def filter_grey(self, word):
        """ returns the grey filter """
        found = []
        for pos_filter in self._grey_filters:
            answer = False
            match = re.match(pos_filter, word)
            if match:
                answer = True
            found.append(answer)

        return not any(found)

        # return any(re.search(f, word) for f in self._grey_filters)

    def green(self, green):
        """ adds green filter to the current guess
            green: b...."""
        self._filter_green = green

    def yellow(self, yellow):
        """ adds yellow characters and input to the current guess
            yellow: ..in."""
        self._yellow_pos_filters.append(
            "".join([f"[^{char}]" if char != "." else char for char in yellow]))
        self._yellow += "".join(char for char in yellow if char != ".")

    def grey(self, grey):
        """ adds grey characters to the current guess """
        self._grey = grey
        self._grey_filters = self.get_soft_filters(self._grey)

    def words(self):
        """ returns the words """
        filtered = self._words
        if self._yellow != "":
            filtered = [word for word in filtered
                        if self.filter_yellow(word)]

        if self._grey != "":
            filtered = [word for word in filtered
                        if self.filter_grey(word)]

        if self._filter_green != "":
            filtered = [word for word in filtered
                        if self.filter_green(word)]
        filtered = sorted(
            filtered, key=lambda word: self.get_num_repeat_chars(word))

        print(filtered)

    def reset(self):
        """ resets greens and yellows """
        self._yellow = ""
        self._filter_green = r""
        self._filterYel = r""

    def debug(self):
        newline = "\n"
        print(f"Green: {self._filter_green}")
        print(f"Yellow Chars: {self._yellow}")
        print(
            f"Yellow filter - Must include these chars: {self._filter_yellow}")
        print(
            f"Yellow Position filters - Just no yellows in these char idxs:\n{newline.join(self._yellow_pos_filters)}")
        print(f"Grey Chars: {self._grey}")
        print(
            f"Grey filters - Don't match these chars:\n{newline.join(self._grey_filters)}")


if __name__ == '__main__':
    wordle = Wordle()   
    wordle.grey("crn")
    wordle.green("a....")
    wordle.yellow("..a.e")
    wordle.yellow("..e..")
    
    wordle()
    # wordle.debug()
    wordle.reset()
