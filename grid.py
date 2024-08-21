import random
from typing import List
from typing import Optional
from typing import Tuple
from cell import Cell
from word import Word
from word_list import WordList


class Grid:
    def __init__(self, grid_size = 15):
        """
        Initialises the grid with the given size.
        """
        self.rows = grid_size
        self.cols = grid_size

        self.wordlists = self.load_word_lists()

        while True:
            while True:
                self._grid = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
                self.words = {
                    "across": {},
                    "down": {}
                }
                self.populate_grid()
                self.assign_numbering()
                self.remove_extra_cells()
                if self.are_lines_connected():
                    self.display_grid()
                    break
            iterable_keys = {
                "across": list(self.words["across"].keys()),
                "down": list(self.words["down"].keys())
            }
            if self.populated_with_words(iterable_keys):
                break

    def load_word_lists(self):
        word_list = WordList()
        return word_list.create_word_lists()


    @property
    def grid(self):
        """
        Provides access to the grid.
        """
        return self._grid
    
    def display_grid(self):
        """
        Displays the grid in a readable format.
        """
        for y in range(self.rows):
            for x in range(self.cols):
                if self._grid[y][x].letter != "#":
                    value = self._grid[y][x].numbering
                    letter = self._grid[y][x].letter
                    # f"{value:02d}" if value is not None else 
                    formatted_value = f" {letter}" if letter is not None else "  "
                    print(f"\033[31;107m{formatted_value}", end = "")
                    print("\033[0m", end = "")
                else:
                    print(f"\033[31;40m  ", end = "")
                    print("\033[0m", end = "")     
            print()

    def populated_with_words(self, iterable_keys, alt_index = 0, across_index = 0, down_index = 0):
        """
        REMEMBER TO POP USED WORDS IN A WAY THAT DOESN'T SCREW WITH THE ITERATION THROUGH WORDS.
        MAYBE PASS A COPY OF WORDLIST TO THE RECURSIVE FUNCTION WITH THE CURRENT WORD REMOVED?
        """
        # Stop populating with words if all across and down indexes have been iterated through
        if across_index == len(iterable_keys["across"]) and down_index == len(iterable_keys["down"]):
            return True
        
        if across_index < len(iterable_keys["across"]) and (down_index >= len(iterable_keys["down"]) or alt_index % 2 == 0):
            direction = "across"
            word_num = iterable_keys["across"][across_index]
            across_index += 1
        else:
            direction = "down"
            word_num = iterable_keys["down"][down_index]
            down_index += 1

        word_length = self.words[direction][word_num].length
        start_y, start_x = self.words[direction][word_num].start_pos
        current_word = []

        for i in range(word_length):
            if direction == "across":
                current_word.append(self._grid[start_y][start_x + i].letter)
            else:
                current_word.append(self._grid[start_y + i][start_x].letter)

        for word in self.wordlists[word_length]:
            valid = True
            for i in range(word_length):
                if current_word[i] and word[i] != current_word[i]:
                    valid = False
            if valid:
                for i in range(word_length):
                    if direction == "across":
                        self._grid[start_y][start_x + i].letter = word[i]
                    else:
                        self._grid[start_y + i][start_x].letter = word[i]
                self.words[direction][word_num].word = word
                self.words[direction][word_num].populated = True
                # Go through each cell in the word, and if it's an intersection, and the intersecting word isn't already populated
                # check whether a valid word can be made in the perpendicular line if it intersects with a letter in the current word.
                for i in range(word_length):
                    if direction == "across":
                        if down_num := self._grid[start_y][start_x + i].num_down:
                            if not self.words["down"][down_num].populated:
                                if not self.can_be_perpendicular("down", down_num):
                                    valid = False
                    else:
                        if across_num := self._grid[start_y + i][start_x].num_across:
                            if not self.words["across"][across_num].populated:
                                if not self.can_be_perpendicular("across", across_num):
                                    valid = False
                if valid:
                    print()
                    self.display_grid()
                    if self.populated_with_words(iterable_keys, alt_index + 1, across_index, down_index):
                        return True

                # Backtrack and erase the word
                self.words[direction][word_num].word = None
                self.words[direction][word_num].populated = False
                for i in range(word_length):
                    if direction == "across":
                        if down_num := self._grid[start_y][start_x + i].num_down:
                            if not self.words["down"][down_num].populated:
                                self._grid[start_y][start_x + i].letter = None
                        else:
                            self._grid[start_y][start_x + i].letter = None
                    else:
                        if across_num := self._grid[start_y + i][start_x].num_across:
                            if not self.words["across"][across_num].populated:
                                self._grid[start_y + i][start_x].letter = None
                        else:
                            self._grid[start_y + i][start_x].letter = None
        return False
    
    def can_be_perpendicular(self, direction: str, word_num: int) -> bool:
        """  
        Checks if a valid word can be placed in a perpendicular line specified by the direction and word_num parameters.  

        Args:  
            direction (str): The direction of the word, either 'across' or 'down'.  
            word_num (int): The index of the word in the specified direction.  
        """  
        word: Word = self.get_word(direction, word_num)
        return self.is_valid_perpendicular_word(word)
    
    def is_valid_perpendicular_word(self, word: Word) -> bool:  
        """  
        Checks if the given word can be placed perpendicularly in the current grid configuration. 

        Args:  
            word (Word): The word object that contains the length and position details.  
        """  
        current_letters: List[Optional[str]] = self.get_current_letters(word)  
        return self.is_valid_word(word.length, current_letters) 
    
    def get_word(self, direction: str, word_num: int) -> Word:  
        """  
        Retrieves the word object from the grid based on direction and index.

        Args:  
            direction (str): The direction of the word, either 'across' or 'down'.  
            word_num (int): The index of the word in the specified direction.  

        Returns:  
            Word: The `Word` object at the given direction and index.  
        """  
        return self.words[direction][word_num]  
    
    def get_current_letters(self, word: Word) -> List[Optional[str]]:
        """
        Retrieves the current letters from the grid corresponding to the given word's position and direction.

        Args:
            word (Word): The word object containing information about its length, start position, and direction.

        Returns:
            List[Optional[str]]: A list of characters representing the current letters on the grid where the word is placed.
                If a cell is has no letter, the corresponding value will be None.
        """
        word_length: int = word.length
        start_y, start_x = word.start_pos
        direction: str = word.direction 
        current_letters: List[Optional[str]] = []
        for i in range(word_length):
            if direction == "across":
                current_letters.append(self._grid[start_y][start_x + i].letter)
            else:
                current_letters.append(self._grid[start_y + i][start_x].letter)
        return current_letters

    def is_valid_word(self, word_length: int, current_letters: List[Optional[str]]) -> bool:
        """
        Checks if a valid word can be formed with the given the letters in a line.

        Args:
            current_letters (List[Optional[str]]): A list of characters representing the current letters in the line.
                                    Empty positions should be represented by None.
        """
        for word in self.wordlists[word_length]:
            valid: bool = True
            for i in range(word_length):
                if current_letters[i] and word[i] != current_letters[i]:
                    valid = False
            if valid:
                return True
        return False
    
    def populate_grid(self):
        """
        Populates the grid with rotationally symmetrical black dividing boxes.
        """
        self.populate_lines("rows")
        self.populate_lines("columns")

    def are_lines_connected(self) -> bool:
        """
        Checks whether all lines in the crossword are connected, and that no breaks exist.
        """
        self.visited: List[List[bool]] = self.initialize_visited_grid()
        coords: Tuple[int, int] = self.get_first_space()
        self.check_line_connections(coords)
        return self.are_all_white_cells_visited()
    
    def initialize_visited_grid(self) -> List[List[bool]]:
        """  
        Initializes the visited grid to track which cells have been checked.

        Returns:
            List[List[bool]]: A 2d list the same size as the grid, filled with the value False.
        """  
        return [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def are_all_white_cells_visited(self) -> bool:
        """
        Checks whether the locations of all of the empty white cells in the grid have also been marked as "visited".
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self._grid[row][col].letter == None and not self.visited[row][col]:
                    return False
        return True
    
    def get_first_space(self) -> Tuple[int, int]:
        """
        Finds the location of the first empty white cell in the grid when iterating from the first cell of the first row to the last cell of the last row.

        Returns:
            Tuple[int, int]: The coordinates of the cell in the form (column number, row number).
        """
        for row in range(self.rows):
            for col in range(self.cols):   
                if self._grid[row][col].letter == None:
                    return (col, row)

    def check_line_connections(self, coords: Tuple[int, int]) -> None:
        """
        Recursively searches surrounding cells to see if they are empty white cells, and marks them as visited.
        
        Args:
            coords (Tuple[int, int]): The coordinates of a blank white space to begin searching from.
        """
        directions: Tuple[Tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))
        current_x: int = coords[0]
        current_y: int = coords[1]
        self.visited[current_y][current_x] = True
        for x, y in directions:
            next_coord: Tuple[int, int] = (current_x + x, current_y + y)
            next_x, next_y = next_coord
            if 0 <= next_x < self.cols and 0 <= next_y < self.rows and self.visited[next_y][next_x] == False and self._grid[next_y][next_x].letter == None:
                self.check_line_connections(next_coord)

    def remove_extra_cells(self):
        """
        Changes any cells that aren't in rows or columns into black squares.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self._grid[row][col].num_across is None and self._grid[row][col].num_down is None:
                    self._grid[row][col].letter = "#"

    def assign_numbering(self) -> None:
        """
        Assigns an incrementing number to cells that begin across and down words.
        """
        number: int = 1
        for row in range(self.rows):
            for col in range(self.cols):
                number_assigned: bool = False
                if self.grid[row][col].letter == None:
                    number_assigned: bool = self.assign_number_to_across_words(row, col, number, number_assigned)
                    number_assigned: bool = self.assign_number_to_down_words(row, col, number, number_assigned)
                    if number_assigned:
                        number += 1

    def assign_number_to_across_words(self, row: int, col: int, number: int, number_assigned: bool) -> bool:
        """
        Assigns a number to a cell at the start of an across word.
        """
        if (col == 0 or self._grid[row][col - 1].letter == "#") and col != self.cols - 1:
            word_length: int = self.get_cell_count_of_word(row, col, "across")
            if word_length >= 3:
                self._grid[row][col].numbering = number
                number_assigned: bool = True
                self.assign_cells_to_word_number(word_length, row, col, number, "across")
                self.add_word_object_to_dictionary("across", number, row, col, word_length)
        return number_assigned
    
    def assign_number_to_down_words(self, row: int, col: int, number: int, number_assigned: bool) -> bool:
        """
        Assigns a number to a cell at the start of a down word.
        """
        if (row == 0 or self._grid[row - 1][col].letter == "#") and row != self.rows - 1:
            word_length: int = self.get_cell_count_of_word(row, col, "down")
            if word_length >= 3:
                self._grid[row][col].numbering = number
                number_assigned: bool = True
                self.assign_cells_to_word_number(word_length, row, col, number, "down")
                self.add_word_object_to_dictionary("down", number, row, col, word_length)
        return number_assigned
    
    def add_word_object_to_dictionary(self, direction: str, number: int, row: int, col: int, word_length: int) -> None:
        """
        Adds and instantiates a Word object to the self.words dictionary.
        """
        self.words[direction][number] = Word(number, direction, (row, col), word_length)
    
    def get_cell_count_of_word(self, row: int, col: int, direction: str) -> int:
        """
        Counts the number of cells in this word starting from the current cell.
        """
        count: int = 0
        if direction == "across":
            while col + count < self.cols and self._grid[row][col + count].letter != "#":
                count += 1
        else:
            while row + count < self.rows and self._grid[row + count][col].letter != "#":
                count += 1
        return count

    def assign_cells_to_word_number(self, word_length: int, row: int, col: int, number: int, direction: str):
        """
        Assigns each cell in a line to the given word number of the given direction.
        """
        for i in range(word_length):
            if direction == "across":
                self._grid[row][col + i].num_across = number
            else:
                self._grid[row + i][col].num_down = number

    def populate_lines(self, orientation: str) -> None:
        """
        Checks for usable space in each first alternating line and divides each space up into smaller word spaces
        using black squares as dividers. On every second line, creates dividers in every second space.

        Args:
            orientation (str): The orientation of the lines being divided (expects "rows" or "columns")
        """
        half_grid: int = len(self._grid) // 2 + 1
        for line in range(half_grid):
            if line % 2 == 0:
                usable_spaces: List[List[int]] = self.find_usable_spaces(line, orientation)
                for usable_space in usable_spaces:
                    first_space, last_space = (usable_space[0], usable_space[1])
                    self.create_word_divisions(first_space, last_space, line, orientation)
            else:
                if orientation == "rows":
                    self.create_alternating_divisions(line)
                    if line != half_grid - 1:
                        # Mirror in the bottom rows
                        self.create_alternating_divisions(len(self._grid) - 1 - line)

    def create_alternating_divisions(self, row):
        """
        Makes every second space in the row a black dividing square.
        """
        for i in range(len(self._grid[row])):
            if i % 2 != 0:
                self._grid[row][i].letter = '#'
    
    def create_word_divisions(self, first_space: int, last_space: int, line: int, orientation: str) -> None:
        """
        Divides up a blank space in a line using black dividing squares according to the chosen
        length of words within that space, and does the same for the equivalent mirrored and axially
        inverted space on the grid.

        Args:
            orientation (str): The orientation of the lines being divided (expects "rows" or "columns")
        """
        word_lengths: List[int] = self.choose_word_lengths(first_space, last_space)
        divisions: List[int] = self.find_division_indexes(first_space, word_lengths)
        self.draw_divisions(divisions, orientation, line)

    def find_division_indexes(self, first_space: int, word_lengths: List[int]) -> List[int]:
        """
        Finds the indexes of all of the grid divisions in the given space based on the word lengths
        that the space is divided up into.

        Args:
            word_lengths (List[int]): The lengths allocated to each word that comprises the current space, in the current line.

        Returns:
            List[int]: The indexes of the black dividing squares.
        """
        divisions: List[int] = []
        # Add the word lengths + 1 to the index before the first space to get the indexes of the divisions
        div_index: int = first_space - 1
        for word_length in word_lengths[:-1]:
            div_index += word_length + 1
            divisions.append(div_index)
        return divisions

    def draw_divisions(self, divisions: List[int], orientation: str, line: int):
        """
        Draws black dividing squares ("#") into a given space according to a list of indexes, and does the same
        for the equivalent horizontally inverted mirrored space in the bottom half of the grid
        if the orientation is "rows". Otherwise does the same for the equivalent vertically
        inverted mirrored space in the right half of the grid if the orientation is "columns".

        Args:
            divisions (List[int]): The indexes of the black dividing squares.
            orientation (str): The orientation of the lines being divided (expects "rows" or "columns")
        """
        for division in divisions:
            end_of_row, end_of_col = (len(self._grid[0]) - 1, len(self._grid) - 1)
            if orientation == "rows":
                self._grid[line][division].letter = '#'
                # Mirror inverted in the bottom rows
                self._grid[end_of_col - line][end_of_row - division].letter = '#'
            else:
                self._grid[division][line].letter = '#'
                # Mirror inverted in the right columns
                self._grid[end_of_col - division][end_of_row - line].letter = '#'

    def choose_word_lengths(self, first_space, last_space):
        """
        Divides a given space up into a random number of spaces and returns the length of those spaces.
        """
        space_length = last_space - first_space + 1
        # Calculate the maximum number of words that can fit in this space
        max_words = ((space_length - 3) // 4) + 1
        # Pick a random number of words to divide this space into
        if max_words == 4:
            num_words = random.choices([1, 2], weights = [5, 100])[0]
        elif max_words == 3:
            num_words = random.randint(1, 2)
        else:
            num_words = 1
        remaining_space = space_length
        word_lengths = []
        # If more than one word, divide the space up into smaller words and black divisions
        if num_words > 1:
            for i in range(num_words):
                # Using the remaining space, create word spaces of random valid sizes
                if i == num_words - 1:
                    word_length = remaining_space
                else:
                    remaining_words = num_words - (i + 1)
                    shortest_word = 3
                    longest_word = remaining_space - (remaining_words * (3 + 1))
                    word_len_range = list(range(shortest_word, longest_word + 1))
                    word_len_weights = [5 if word_len == 3 or (remaining_space - word_len == (3 + 1)) else 100 for word_len in word_len_range]
                    word_length = random.choices(word_len_range, weights = word_len_weights)[0]
                    # Deduct word length and a single space from remaining space
                    remaining_space -= word_length + 1
                # Save the word lengths to a list
                word_lengths.append(word_length)
        else:
            # If only one word, return
            word_lengths.append(remaining_space)
        return word_lengths
    
    def find_usable_spaces(self, line: int, orientation: str, is_space: bool = False, first_space: int = 0, last_space: int = 0) -> List[List[int]]:
        """
        Finds all usable spaces in a line and returns a list with the first and last index of each space.

        Args:
            orientation (str): The orientation of the lines being divided (expects "rows" or "columns")

        Returns:
            List[List[int]]: A list of lists containing the indexes of the first and last cells in each space, with each inner list
                                representing each space.
        """
        usable_spaces: List[List[int]] = []
        for pos in range(self.rows):
            if not is_space:
                is_space, first_space = self.find_first_space(pos, is_space, first_space, line, orientation)
            else:
                if orientation == "rows":
                    is_space = self.find_last_space_rows(pos, is_space, first_space, last_space, line, usable_spaces)
                else:
                    is_space = self.find_last_space_cols(pos, is_space, first_space, last_space, line, usable_spaces)
        return usable_spaces
    
    def find_first_space(self, pos: int, is_space: bool, first_space: int, line: int, orientation: str) -> Tuple[bool, int]:
        """
        Finds the next cell that begins a space within the current line. Returns the index of this space and sets the boolean
        "space" to True, signalling that the space has been started.

        Args:
            orientation (str): The orientation of the lines being divided (expects "rows" or "columns")

        Returns:
            Tuple[bool, int]: A boolean that flags whether what is being iterated through is a space, and the index of the first space.
        """
        if orientation == "rows":
            if self._grid[line][pos].letter == None:
                is_space: bool = True
                first_space: int = pos
        else:
            if self._grid[pos][line].letter == None:
                is_space: bool = True
                first_space: int = pos
        return is_space, first_space
    
    def find_last_space_rows(self, pos: int, is_space: bool, first_space: int, last_space: int, line: int, usable_spaces: List[List[int]]) -> bool:
        """
        Finds the last cell in the current space, whether due to the next cell being a black square or because the end of the row has been reached.
        Appends the first and last spaces to a list and sets the boolean "space" to False, signalling that the space has ended.

        Args:
            usable_spaces (List[List[int]]): A list of lists containing the indexes of the first and last cells in each space, with each inner list
                                representing each space.
        """
        # Black square
        if self._grid[line][pos].letter != None:
            is_space: bool = False
            last_space: int = pos - 1
            if last_space - first_space >= 3:
                usable_spaces.append((first_space, last_space))
        else:
            # Last space in the row, with preceeding spaces
            if pos == self.rows - 1:
                last_space: int = pos
                if last_space - first_space >= 3:
                    usable_spaces.append((first_space, last_space))
        return is_space
    
    def find_last_space_cols(self, pos: int, is_space: bool, first_space: int, last_space: int, line: int, usable_spaces: List[List[int]]) -> bool:
        """
        Finds the last cell in the current space, whether due to the next cell being a black square or because the end of the column has been reached.
        Appends the first and last spaces to a list and sets the boolean "space" to False, signalling that the space has ended.

        Args:
            usable_spaces (List[List[int]]): A list of lists containing the indexes of the first and last cells in each space, with each inner list
                                representing each space.
        """
        # Black square
        if self._grid[pos][line].letter != None:
            is_space: bool = False
            last_space: int = pos - 1
            if last_space - first_space >= 3:
                usable_spaces.append((first_space, last_space))
        else:
            # Last space in the column, with preceeding spaces
            if pos == self.cols - 1:
                last_space: int = pos
                if last_space - first_space >= 3:
                    usable_spaces.append((first_space, last_space))
        return is_space