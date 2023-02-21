"""Responsible for storing the current game's information,
for determining valid moves for the current state and a history of the moves taken
"""
# Imports
import numpy as np


class GameState():
    """Class for the game state."""

    def __init__(self):
        """Sets up the board, whose move it is and a movelog

        Sets up the board as an 8x8 Numpy 2d array. Each piece is represented by 2 characters,
        the first character represents the colour, second character represents piece:
        R = Rook, N = Knight, B = Bishop, Q = Queen and K = King. -- represents empty space.
        """

        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ])

        self.white_to_move: bool = True

        self.movelog = []
    

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.movelog.append(move) # Add to log
        self.white_to_move = not self.white_to_move # Swap turn


class Move():
    """A class for moving the pieces and chess notation convertions"""

    # Maps keys to values, ranks and files special chess words for same thing
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}
    
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                    "e": 4, "f": 5, "g": 6, "h":7}
    
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq: tuple[int, int], end_sq: tuple[int, int], board):
        """Setup all the coordinate stuff"""

        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]


    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)
    

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
