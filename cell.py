class Cell:
    def __init__(self):

        self.letter = None # None for blank, "#" for black square, or a letter
        self.numbering = None # None or the number of the clue
        self.num_across = None # Reference to the across word number
        self.num_down = None # Reference to the down word number
        self.word_across = None # Word object of across word that cell is a member of
        self.word_down = None # Word object of down word that cell is a member of

    def __str__(self):
        """
        Displays instance variables when the cell object is printed.
        """
        letter = f"self.letter = {self.letter}"
        number = f"self.numbering = {self.numbering}"
        across = f"self.num_across = {self.num_across}"
        down = f"self.num_down = {self.num_down}"
        return f"{letter}, {number}, {across}, {down}"