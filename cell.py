from typing import Optional
from word import Word

class Cell:
    def __init__(self):
        self.letter: Optional[str] = None # None for blank, "#" for black square, or a letter
        self.numbering: Optional[int] = None # None or the number of the clue
        self.num_across: Optional[int] = None # Reference to the across word number
        self.num_down: Optional[int] = None # Reference to the down word number
        self.word_across: Optional[Word] = None # Word object corresponding to this cell's across word, or None
        self.word_down: Optional[Word] = None # Word object corresponding to this cell's down word, or None

    def __str__(self):
        """
        Displays instance variables when the cell object is printed.
        """
        letter: Optional[str] = f"self.letter = {self.letter}"
        number: Optional[int] = f"self.numbering = {self.numbering}"
        across: Optional[int] = f"self.num_across = {self.num_across}"
        down: Optional[int] = f"self.num_down = {self.num_down}"
        return f"{letter}, {number}, {across}, {down}"