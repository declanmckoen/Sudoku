import math, random, copy
import pygame, sys
from constants import *


class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]
        self.box_length = int(math.sqrt(row_length))

    def get_board(self):
        return self.board

    def print_board(self):
        for i in self.board:
            for e in i:
                print(e, end=" ")
            print()

    def valid_in_row(self, row, num):
        return False if num in self.board[row] else True

    def valid_in_col(self, col, num):
        for row in self.board:
            if row[col] == num:
                return False
        return True

    def valid_in_box(self, row_start, col_start, num):
        box = [[e for e in rows[col_start:col_start + 3]] for rows in self.board[row_start:row_start + 3]]

        for row in box:
            if num in row:
                return False

        return True

    def is_valid(self, row, col, num):
        valid_in_row = False
        valid_in_col = False
        valid_in_box = False

        if self.valid_in_row(row, num):
            valid_in_row = True

        if self.valid_in_col(col, num):
            valid_in_col = True

        if 0 <= row < 3:
            row = 0
        elif 3 <= row < 6:
            row = 3
        elif 6 <= row < 9:
            row = 6

        if 0 <= col < 3:
            col = 0
        elif 3 <= col < 6:
            col = 3
        elif 6 <= col < 9:
            col = 6

        if self.valid_in_box(row, col, num):
            valid_in_box = True

        return valid_in_row and valid_in_col and valid_in_box

    def fill_diagonal(self):
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(nums)
        for row in range(3):
            for col in range(3):
                rand_int = nums.pop()
                self.board[row][col] = rand_int

        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(nums)
        for row in range(3, 6):
            for col in range(3, 6):
                rand_int = nums.pop()
                self.board[row][col] = rand_int

        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(nums)
        for row in range(6, 9):
            for col in range(6, 9):
                rand_int = nums.pop()
                self.board[row][col] = rand_int

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):
        for i in range(self.removed_cells):
            while True:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
                if self.board[row][col] != 0:
                    self.board[row][col] = 0
                    break

    @staticmethod
    def generate_sudoku(size, removed):
        sudoku = SudokuGenerator(size, removed)
        sudoku.fill_values()
        board = sudoku.get_board()
        sudoku.remove_cells()
        board = sudoku.get_board()
        return board


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = None
        self.user_val = None
        self.selected = False
        self.user_val = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        # red outline
        if self.selected:
            pygame.draw.rect(self.screen, RED, pygame.Rect(SQUARE_SIZE * self.col, SQUARE_SIZE * self.row, SQUARE_SIZE, SQUARE_SIZE), 4)
            self.selected = False

        # drawing the cell
        num_font = pygame.font.Font(None, 50)
        digit_surf = num_font.render(str(self.value), 0, DIGIT_COLOR)
        user_val_surf = num_font.render(str(self.user_val), 0, SKETCHED_COLOR)
        sketched_surf = num_font.render(str(self.sketched_value), 0, SKETCHED_COLOR)

        if self.value > 0:
            digit_rect = digit_surf.get_rect(center=(self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2))
            self.screen.blit(digit_surf, digit_rect)
        if self.sketched_value is not None:
            sketched_rect = sketched_surf.get_rect(center=(self.col * SQUARE_SIZE + SQUARE_SIZE // 3, self.row * SQUARE_SIZE + SQUARE_SIZE // 3))
            self.screen.blit(sketched_surf, sketched_rect)


class ModifiableCell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = None
        self.selected = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        # red outline
        if self.selected:
            pygame.draw.rect(self.screen, RED, pygame.Rect(SQUARE_SIZE * self.col, SQUARE_SIZE * self.row, SQUARE_SIZE, SQUARE_SIZE), 4)
            self.selected = False

        # drawing the cell
        num_font = pygame.font.Font(None, 50)
        digit_surf = num_font.render(str(self.value), 0, SKETCHED_COLOR)
        sketched_surf = num_font.render(str(self.sketched_value), 0, SKETCHED_COLOR)

        if self.value > 0:
            digit_rect = digit_surf.get_rect(center=(self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2))
            self.screen.blit(digit_surf, digit_rect)
        if self.sketched_value is not None:
            sketched_rect = sketched_surf.get_rect(center=(self.col * SQUARE_SIZE + SQUARE_SIZE // 3, self.row * SQUARE_SIZE + SQUARE_SIZE // 3))
            self.screen.blit(sketched_surf, sketched_rect)


class Board():
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.selected_cell = None
        self.row = None
        self.col = None

        sudoku = SudokuGenerator(9, difficulty)
        sudoku.fill_values()
        self.solution = copy.deepcopy(sudoku.get_board())
        sudoku.remove_cells()
        self.board = sudoku.get_board()
        self.modifiable_board = copy.deepcopy(self.board)
        self.cells = [[Cell(col, row_pos, col_pos, self.screen) for col_pos, col in enumerate(row)]for row_pos, row in enumerate(self.modifiable_board)]

    def draw(self):
        self.screen.fill(BG_COLOR)
        # vertical lines
        for i in range(1, BOARD_COLS):
            pygame.draw.line(self.screen, LINE_COLOR, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

        # horizontal lines
        for i in range(1, BOARD_ROWS):
            pygame.draw.line(self.screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)

        # vertical darkened lines
        for i in range(1, 3):
            pygame.draw.line(self.screen, DARKENED_LINE_COLOR, (WIDTH // 3 * i, 0), (WIDTH // 3 * i, HEIGHT), LINE_WIDTH)

        # horizontal darkened lines
        for i in range(1, 3):
            pygame.draw.line(self.screen, DARKENED_LINE_COLOR, (0, HEIGHT // 3 * i), (WIDTH, HEIGHT // 3 * i), LINE_WIDTH)

        # outer border
        pygame.draw.rect(self.screen, DARKENED_LINE_COLOR,
                         pygame.Rect(0, 0, WIDTH, HEIGHT), 7)

        # each individual cell
        for i in range(9):
            for j in range(9):
                self.cells[i][j].draw()

    def select(self, row, col):
        self.cells[row][col].selected = True
        self.cells[row][col].draw()
        self.selected_cell = self.board[row][col]

    def click(self, x, y):
        if x < 801 and y < 801:
            row = y // SQUARE_SIZE
            col = x // SQUARE_SIZE
            self.row = row
            self.col = col
            return col, row

    def clear(self):
        if self.selected_cell == 0:
            self.modifiable_board[self.row][self.col] = 0

    def sketch(self, value):
        if self.selected_cell == 0:
            self.cells[self.row][self.col].sketched_value = value
            self.cells[self.row][self.col].draw()

    def place_number(self, value):
        if self.selected_cell == 0:
            self.modifiable_board[self.row][self.col] = value

    def reset_to_original(self):
        for i in range(len(self.modifiable_board)):
            for e in range(len(self.modifiable_board)):
                self.modifiable_board[i][e] = self.board[i][e]

    def is_full(self):
        for row in self.modifiable_board:
            for j in row:
                if j == 0:
                    return False
        return True

    def update_board(self):
        self.cells = [[ModifiableCell(col, row_pos, col_pos, self.screen)
                       if self.board[row_pos][col_pos] == 0 else Cell(col, row_pos, col_pos, self.screen)
                       for col_pos, col in enumerate(rows)] for row_pos, rows in enumerate(self.modifiable_board)]
        self.draw()

    def find_empty(self):
        pass

    def check_board(self):
        for i in range(len(self.modifiable_board)):
            for j in range(len(self.modifiable_board)):
                if self.modifiable_board[i][j] != self.solution[i][j]:
                    return False
        return True