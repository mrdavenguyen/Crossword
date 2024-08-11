import random
from cell import Cell
from word import Word
from wordlist import WordList


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
                if self.lines_connected():
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
                                if not self.perpendicular_word_valid("down", down_num):
                                    valid = False
                    else:
                        if across_num := self._grid[start_y + i][start_x].num_across:
                            if not self.words["across"][across_num].populated:
                                if not self.perpendicular_word_valid("across", across_num):
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
    
    def perpendicular_word_valid(self, direction, word_num):
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
                return True
        return False


    def iterate_word_index(self, iterable_keys, direction, key_index):
        if key_index < len(iterable_keys[direction]) - 1:
            key_index += 1
        else:
            direction = "down"
            key_index = 0
        return direction, key_index
    
    def populate_grid(self):
        """
        Fills the blank space in the grid with black dividing boxes.
        """
        self.populate_rows()
        self.populate_columns()

    def lines_connected(self):
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        coords = self.get_first_space()
        self.check_line_connections(coords)
        for row in range(self.rows):
            for col in range(self.cols):
                if self._grid[row][col].letter == None and not self.visited[row][col]:
                    return False
        return True
    
    def get_first_space(self):
        for row in range(self.rows):
            for col in range(self.cols):   
                if self._grid[row][col].letter == None:
                    return (col, row)

    def check_line_connections(self, coords):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        current_x = coords[0]
        current_y = coords[1]
        self.visited[current_y][current_x] = True
        for x, y in directions:
            next_coord = (current_x + x, current_y + y)
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

    def assign_numbering(self):
        """
        Assigns numbers to cells that begin across and down words, and give cells membership to these
        numbered words.
        """
        number = 1
        for row in range(self.rows):
            for col in range(self.cols):
                number_assigned = False
                if self.grid[row][col].letter == None:
                    if (col == 0 or self._grid[row][col - 1].letter == "#") and col != self.cols - 1:
                        # Count the number of cells in this word (left to right), starting from the current cell
                        count = 0
                        while col + count < self.cols and self._grid[row][col + count].letter != "#":
                            count += 1
                        if count >= 3:
                            self._grid[row][col].numbering = number
                            number_assigned = True
                            # Assign membership to across word
                            for i in range(count):
                                self._grid[row][col + i].num_across = number
                            # Add across word to the dictionary
                            self.words["across"][number] = Word(number, "across", (row, col), count)
                    if (row == 0 or self._grid[row - 1][col].letter == "#") and row != self.rows - 1:
                        # Count the number of cells in this word (top to bottom), starting from the current cell
                        count = 0
                        while row + count < self.rows and self._grid[row + count][col].letter != "#":
                            count += 1
                        if count >= 3:
                            self._grid[row][col].numbering = number
                            number_assigned = True
                            # Assign membership to down word
                            for i in range(count):
                                self._grid[row + i][col].num_down = number
                            # Add down word to the dictionary
                            self.words["down"][number] = Word(number, "down", (row, col), count)
                    if number_assigned:
                        number += 1

    def populate_columns(self):
        """
        Checks for usable space in each column and divides each space up into smaller word spaces
        using black squares as dividers.
        """
        if len(self._grid) % 2 == 0:
            half_grid = len(self._grid[0]) // 2
        else:
            half_grid = len(self._grid[0]) // 2 + 1
        for col in range(half_grid):
            if col % 2 == 0:
                usable_spaces = self.get_usable_spaces_cols(col)
                for usable_space in usable_spaces:
                    first_space = usable_space[0]
                    last_space = usable_space[1]
                    self.create_word_divisions_cols(first_space, last_space, col)

    def populate_rows(self):
        """
        Checks for usable space in each row and divides each space up into smaller word spaces
        using black squares as dividers.
        """
        if len(self._grid) % 2 == 0:
            half_grid = len(self._grid) // 2
        else:
            half_grid = len(self._grid) // 2 + 1
        for row in range(half_grid):
            if row % 2 == 0:
                usable_spaces = self.get_usable_spaces(row)
                for usable_space in usable_spaces:
                    first_space = usable_space[0]
                    last_space = usable_space[1]
                    self.create_word_divisions(first_space, last_space, row)
            else:
                self.create_alternating_divisions(row)
                if row != half_grid - 1:
                    # Mirror in the bottom rows
                    self.create_alternating_divisions(len(self._grid) - 1 - row)

    def create_alternating_divisions(self, row):
        """
        Makes every second space in the row a black dividing square.
        """
        for i in range(len(self._grid[row])):
            if i % 2 != 0:
                self._grid[row][i].letter = '#'
    
    def create_word_divisions(self, first_space, last_space, row):
        """
        Divides up a blank space in a row using black dividing squares, and does the same
        for the equivalent horizontally inverted mirrored space in the bottom half of the grid.
        """
        word_lengths = self.choose_word_lengths(first_space, last_space)
        divisions = []
        # Add the word lengths + 1 to the index before the first space to get the indexes of the divisions
        div_index = first_space - 1
        for word_length in word_lengths[:-1]:
            div_index += word_length + 1
            divisions.append(div_index)
        for division in divisions:
            end_of_row = len(self._grid[row]) - 1
            end_of_col = len(self._grid) - 1
            self._grid[row][division].letter = '#'
            # Mirror inverted in the bottom rows
            self._grid[end_of_col - row][end_of_row - division].letter = '#'

    def create_word_divisions_cols(self, first_space, last_space, col):
        """
        Divides up a blank space in a column using black dividing squares, and does the same
        for the equivalent vertically inverted mirrored space in the right half of the grid.
        """
        word_lengths = self.choose_word_lengths(first_space, last_space)
        divisions = []
        # Add the word lengths + 1 to the index before the first space to get the indexes of the divisions
        div_index = first_space - 1
        for word_length in word_lengths[:-1]:
            div_index += word_length + 1
            divisions.append(div_index)
        for division in divisions:
            end_of_row = len(self._grid[0]) - 1
            end_of_col = len(self._grid) - 1
            self._grid[division][col].letter = '#'
            # Mirror inverted in the right columns
            self._grid[end_of_col - division][end_of_row - col].letter = '#'

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

    def get_usable_spaces(self, row):
        """
        Finds all usable spaces in a row and returns a list with the first and last index of each space. 
        """
        usable_spaces = []
        space = False
        first_space = 0
        last_space = 0
        row_length = len(self._grid[row])
        for i in range(row_length):
            if space == False:
                # First space, or first after a black square
                if self._grid[row][i].letter == None:
                    space = True
                    first_space = i
            else:
                # Black square
                if self._grid[row][i].letter != None:
                    space = False
                    last_space = i - 1
                    if last_space - first_space >= 3:
                        usable_spaces.append([first_space, last_space])
                else:
                    # Last space in the row, with preceeding spaces
                    if i == row_length - 1:
                        last_space = i
                        if last_space - first_space >= 3:
                            usable_spaces.append([first_space, last_space])
        return usable_spaces
    
    def get_usable_spaces_cols(self, col):
        """
        Finds all usable spaces in a column and returns a list with the first and last index of each space. 
        """
        usable_spaces = []
        space = False
        first_space = 0
        last_space = 0
        col_length = len(self._grid)
        for i in range(col_length):
            if space == False:
                # First space, or first after a black square
                if self._grid[i][col].letter == None:
                    space = True
                    first_space = i
            else:
                # Black square
                if self._grid[i][col].letter != None:
                    space = False
                    last_space = i - 1
                    if last_space - first_space >= 3:
                        usable_spaces.append([first_space, last_space])
                else:
                    # Last space in the row, with preceeding spaces
                    if i == col_length - 1:
                        last_space = i
                        if last_space - first_space >= 3:
                            usable_spaces.append([first_space, last_space])
        return usable_spaces