from typing import List, Tuple

class Word:
    def __init__(self, number: int, direction: str, start_pos: Tuple[int, int], length: int):
        self.number: int = number # Number assigned to the word
        self.direction: str = direction # across or down
        self.start_pos: Tuple[int, int] = start_pos # Coordinates of the first letter of the word
        self.length: int = length # Length of the word
        self.word: str = None # The word assigned from the word list
        self.populated: bool = False # Indicates whether the word space has been populated with letters or not
        self.cells: List[Tuple[int, int]] = [] # Coordinates of all cells in the word

    def __repr__(self):
        return self.word