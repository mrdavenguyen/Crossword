class Word:
    def __init__(self, number, direction, start_pos, length):
        self.number = number # Number assigned to the word
        self.direction = direction # across or down
        self.start_pos = start_pos # Tuple (row, col) coordinates
        self.length = length # Length of the word
        self.word = None
        self.populated = False # Boolean indicating if the word is populated

def __repr__(self):
    return self.word