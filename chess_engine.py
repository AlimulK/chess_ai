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


class Move():
    """A class for moving the pieces"""

    def __init__(self, start_sq: tuple[int, int], end_sq: tuple[int, int], board):
        """Setup all the coordinate stuff"""

        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

    