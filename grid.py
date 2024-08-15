import random
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
        """
        Checks if a valid word can be made in a perpendicular line specified by the direction and word_num parameters.
        """
        word_length = self.words[direction][word_num].length
        start_y, start_x = self.words[direction][word_num].start_pos
        current_letters = self.collect_current_letters(word_length, start_y, start_x, direction)
        return self.valid_word(word_length, current_letters)
    
    def collect_current_letters(self, word_length, start_y, start_x, direction):
        """
        Provides a list of letters in the current line.
        """
        current_letters = []
        for i in range(word_length):
            if direction == "across":
                current_letters.append(self._grid[start_y][start_x + i].letter)
            else:
                current_letters.append(self._grid[start_y + i][start_x].letter)
        return current_letters

    def valid_word(self, word_length, current_letters):
        """
        Checks if a valid word can be made given the current letters in a line.
        """
        for word in self.wordlists[word_length]:
            valid = True
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

    def lines_connected(self):
        """
        Checks whether all lines in the crossword are connected, and that no breaks exist.
        """
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        coords = self.get_first_space()
        self.check_line_connections(coords)
        return self.all_spaces_visited()

    def all_spaces_visited(self):
        """
        Checks whether the locations of all of the empty white cells in the grid have also been marked as "visited".
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self._grid[row][col].letter == None and not self.visited[row][col]:
                    return False
        return True
    
    def get_first_space(self):
        """
        Finds the location of the first empty white cell in the grid when iterating from the first cell of the first row to the last cell of the last row.
        """
        for row in range(self.rows):
            for col in range(self.cols):   
                if self._grid[row][col].letter == None:
                    return (col, row)

    def check_line_connections(self, coords):
        """
        Recursively searches surrounding cells to see if they are empty white cells, and marks them as visited.
        """
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
        Assigns an incrementing number to cells that begin across and down words.
        """
        number = 1
        for row in range(self.rows):
            for col in range(self.cols):
                number_assigned = False
                if self.grid[row][col].letter == None:
                    number_assigned = self.assign_across_numbering(row, col, number, number_assigned)
                    number_assigned = self.assign_down_numbering(row, col, number, number_assigned)
                    if number_assigned:
                        number += 1

    def assign_across_numbering(self, row, col, number, number_assigned):
        """
        Assigns a number to a cell at the start of an across word.
        """
        if (col == 0 or self._grid[row][col - 1].letter == "#") and col != self.cols - 1:
            word_length = self.count_cells_in_word(row, col, "across")
            if word_length >= 3:
                self._grid[row][col].numbering = number
                number_assigned = True
                self.assign_membership_to_word(word_length, row, col, number, "across")
                self.add_word_object_to_dictionary("across", number, row, col, word_length)
        return number_assigned
    
    def assign_down_numbering(self, row, col, number, number_assigned):
        """
        Assigns a number to a cell at the start of a down word.
        """
        if (row == 0 or self._grid[row - 1][col].letter == "#") and row != self.rows - 1:
            word_length = self.count_cells_in_word(row, col, "down")
            if word_length >= 3:
                self._grid[row][col].numbering = number
                number_assigned = True
                self.assign_membership_to_word(word_length, row, col, number, "down")
                self.add_word_object_to_dictionary("down", number, row, col, word_length)
        return number_assigned
    
    def add_word_object_to_dictionary(self, direction, number, row, col, word_length):
        """
        Adds and instantiates a Word object to the self.words dictionary.
        """
        self.words[direction][number] = Word(number, direction, (row, col), word_length)
    
    def count_cells_in_word(self, row, col, direction):
        """
        Counts the number of cells in this word starting from the current cell.
        """
        count = 0
        if direction == "across":
            while col + count < self.cols and self._grid[row][col + count].letter != "#":
                count += 1
        else:
            while row + count < self.rows and self._grid[row + count][col].letter != "#":
                count += 1
        return count

    def assign_membership_to_word(self, word_length, row, col, number, direction):
        """
        Assigns each cell in a word to the given word number.
        """
        for i in range(word_length):
            if direction == "across":
                self._grid[row][col + i].num_across = number
            else:
                self._grid[row + i][col].num_down = number

    def populate_lines(self, orientation):
        """
        Checks for usable space in each first alternating line and divides each space up into smaller word spaces
        using black squares as dividers. On every second line, creates dividers in every second space.
        """
        half_grid = len(self._grid) // 2 + 1
        for line in range(half_grid):
            if line % 2 == 0:
                usable_spaces = self.find_usable_spaces(line, orientation)
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
    
    def create_word_divisions(self, first_space, last_space, line, orientation):
        """
        Divides up a blank space in a line using black dividing squares according to the chosen
        length of words within that space, and does the same for the equivalent mirrored and axially
        inverted space on the grid.
        """
        word_lengths = self.choose_word_lengths(first_space, last_space)
        divisions = self.find_division_indexes(first_space, word_lengths)
        self.draw_divisions(divisions, orientation, line)


    def find_division_indexes(self, first_space, word_lengths):
        """
        Finds the indexes of all of the grid divisions in the given space based on the word lengths
        that the space is divided up into.
        """
        divisions = []
        # Add the word lengths + 1 to the index before the first space to get the indexes of the divisions
        div_index = first_space - 1
        for word_length in word_lengths[:-1]:
            div_index += word_length + 1
            divisions.append(div_index)
        return divisions

    def draw_divisions(self, divisions, orientation, line):
        """
        Draws black dividing squares ("#") into a given space according to a list of indexes, and does the same
        for the equivalent horizontally inverted mirrored space in the bottom half of the grid
        if the orientation is "rows". Otherwise does the same for the equivalent vertically
        inverted mirrored space in the right half of the grid if the orientation is "columns".
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
        remaining_space = last_space - first_space + 1
        num_words = self.calculate_number_of_words(remaining_space)
        word_lengths = []
        # If more than one word, divide the space up into smaller words and black divisions
        if num_words > 1:
            self.create_random_word_lengths(remaining_space, num_words, word_lengths)
        else:
            # If only one word, return
            word_lengths.append(remaining_space)
        return word_lengths
    
    def calculate_number_of_words(self, space_length):
        """
        Calculates the maximum number of words that can fit in a space of specified length.
        """
        max_words = ((space_length - 3) // 4) + 1
        # Pick a random number of words to divide this space into
        if max_words == 4:
            return random.choices([1, 2], weights = [5, 100])[0]
        elif max_words == 3:
            return random.randint(1, 2)
        else:
            return 1

    def create_random_word_lengths(self, remaining_space, num_words, word_lengths):
        """
        Creates word spaces of random lengths with each having a minimum length of 3.
        """
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
            word_lengths.append(word_length)
    
    def find_usable_spaces(self, line, orientation, space=False, first_space=0, last_space=0):
        """
        Finds all usable spaces in a line and returns a list with the first and last index of each space. 
        """
        usable_spaces = []
        for pos in range(self.rows):
            if not space:
                space, first_space = self.find_first_space(pos, space, first_space, line, orientation)
            else:
                if orientation == "rows":
                    space = self.find_last_space_rows(pos, space, first_space, last_space, line, usable_spaces)
                else:
                    space = self.find_last_space_cols(pos, space, first_space, last_space, line, usable_spaces)
        return usable_spaces
    
    def find_first_space(self, pos, space, first_space, line, orientation):
        """
        Finds the next cell that begins a space within the current line. Returns the index of this space and sets the boolean
        "space" to True, signalling that the space has been started.
        """
        if orientation == "rows":
            if self._grid[line][pos].letter == None:
                space = True
                first_space = pos
        else:
            if self._grid[pos][line].letter == None:
                space = True
                first_space = pos
        return space, first_space
    
    def find_last_space_rows(self, pos, space, first_space, last_space, line, usable_spaces):
        """
        Finds the last cell in the current space, whether due to the next cell being a black square or because the end of the row has been reached.
        Appends the first and last spaces to a list and sets the boolean "space" to False, signalling that the space has ended.
        """
        # Black square
        if self._grid[line][pos].letter != None:
            space = False
            last_space = pos - 1
            if last_space - first_space >= 3:
                usable_spaces.append((first_space, last_space))
        else:
            # Last space in the row, with preceeding spaces
            if pos == self.rows - 1:
                last_space = pos
                if last_space - first_space >= 3:
                    usable_spaces.append((first_space, last_space))
        return space
    
    def find_last_space_cols(self, pos, space, first_space, last_space, line, usable_spaces):
        """
        Finds the last cell in the current space, whether due to the next cell being a black square or because the end of the column has been reached.
        Appends the first and last spaces to a list and sets the boolean "space" to False, signalling that the space has ended.
        """
        # Black square
        if self._grid[pos][line].letter != None:
            space = False
            last_space = pos - 1
            if last_space - first_space >= 3:
                usable_spaces.append((first_space, last_space))
        else:
            # Last space in the column, with preceeding spaces
            if pos == self.cols - 1:
                last_space = pos
                if last_space - first_space >= 3:
                    usable_spaces.append((first_space, last_space))
        return space