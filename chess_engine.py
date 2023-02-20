"""Responsible for storing the current game's information,
for determining valid moves for the current state and a history of the moves taken
"""

import numpy as np

class GameState():
    """Class for the game state, initialises the board."""

    def __init__(self) -> None:
        """Sets up the board

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
