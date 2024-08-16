import pygame


class Cell(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.x = None
        self.y = None
        self.color = None

        self.size = 50
        self.letter_font = pygame.font.SysFont("Trebuchet", (self.size // 5) * 4)
        self.number_font = pygame.font.SysFont("Trebuchet", (self.size // 5) * 2)

        self.image = pygame.Surface((self.size, self.size))
        self.rect = self.image.get_rect()

        self.letter = None  # None for blank, "#" for black square, or a letter
        self.numbering = None  # None or the number of the clue
        self.num_across = None  # Reference to the across word number
        self.num_down = None  # Reference to the down word number

    def __str__(self):
        """Displays instance variables when the cell object is printed."""
        letter = f"self.letter = {self.letter}"
        number = f"self.numbering = {self.numbering}"
        across = f"self.num_across = {self.num_across}"
        down = f"self.num_down = {self.num_down}"
        return f"{letter}, {number}, {across}, {down}"

    def set_cell_color(self):
        if self.letter == "#":
            self.color = "black"
        else:
            self.color = "white"

    def set_position(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def set_cell_position(self):
        # Set the position of the cell
        self.rect.topleft = (self.x, self.y)

    def display_number_on_cell(self):
        text_surface = self.number_font.render(
            str(self.numbering), True, (0, 0, 0)
        )  # Render the letter in black color

        # Center the text on the square surface
        text_rect = text_surface.get_rect(topleft=(self.size // 20, self.size // 20))

        self.image.blit(
            text_surface, text_rect
        )  # Blit the text onto the square surface

    def display_letter_on_cell(self):
        text_surface = self.letter_font.render(
            self.letter.upper(), True, (0, 0, 0)
        )  # Render the letter in black color

        # Center the text on the square surface
        text_rect = text_surface.get_rect(center=(self.size // 2, self.size // 2))

        self.image.blit(
            text_surface, text_rect
        )  # Blit the text onto the square surface

    def clear_cell(self):
        self.image = pygame.Surface((self.size, self.size))
        self.rect = self.image.get_rect()
        self.draw_cell()
        self.set_cell_position()
        self.set_cell_color()

    def draw_cell(self):
        pygame.draw.rect(
            self.image, self.color, (0, 0, self.size, self.size), border_radius=10
        )

    def update_cell(self):
        self.set_cell_position()
        self.set_cell_color()
        self.draw_cell()
        self.display_letter_on_cell()
        if self.numbering != None:
            self.display_number_on_cell()
