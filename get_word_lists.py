import random

# def main():
#     word_lists = create_word_lists()

class GetWordList:

    def __init__(self, filename="words_alpha.txt"):
        """
        Initializes the WordListManager with the path to the word list file.
        """
        self.filename = filename
        self.word_lists = self.create_word_lists()

    def create_word_lists(self):
        word_lists = {i: [] for i in range(3, 16)}
        with open("words_alpha.txt") as file:
            for word in file:
                word = word.strip()
                if 3 <= len(word) <= 15:
                    word_lists[len(word)].append(word)
        for length in word_lists:
            random.shuffle(word_lists[length])
        return word_lists