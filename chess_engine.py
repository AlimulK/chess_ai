"""Responsible for storing the current game's information,
for determining valid moves for the current state and a history of the moves taken
"""
# Imports
import numpy as np


class GameState:
    """Class for the game state"""

    def __init__(self):
        """Sets up the board, whose move it is and a movelog

        Sets up the board as a 8x8 Numpy 2d array. Each piece is represented by 2 characters,
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

        self.movelog: list = []

    def make_move(self, move):
        """This doesn't work for special moves, like castling or en passant"""

        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.movelog.append(move)  # Add to log
        self.white_to_move = not self.white_to_move  # Swap turn

    def undo_move(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    def all_moves(self):
        """All moves that are possible, following the rules"""

        moves = []
        for r in range(len(self.board)):  # Rows
            for c in range(len(self.board[r])):  # Cols
                turn = self.board[r][c][0]
                if (turn == "w" and self.white_to_move) and (turn == "b" and not self.white_to_move):
                    piece = self.board[r][c][1]
                    if piece == "P":
                        self.pawn_move(r, c, moves)
                    elif piece == "R":
                        self.rook_move(r, c, moves)
                    elif piece == "N":
                        self.knight_move(r, c, moves)
                    elif piece == "B":
                        self.bishop_move(r, c, moves)
                    elif piece == "Q":
                        self.queen_move(r, c, moves)
                    elif piece == "K":
                        self.king_move(r, c, moves)

        return moves

    def pawn_move(self, r, c, moves):
        """The valid moves a pawn can make"""

        pass

    def rook_move(self, r, c, moves):
        """The valid moves a rook can make"""

        pass

    def knight_move(self, r, c, moves):
        """The valid moves a knight can make"""

        pass

    def bishop_move(self, r, c, moves):
        """The valid moves a bishop can make"""

        pass

    def queen_move(self, r, c, moves):
        """The valid moves a queen can make"""

        pass

    def king_move(self, r, c, moves):
        """The valid moves a king can make"""

        pass

    def check_moves(self):
        """All moves taking check into consideration"""

        return self.all_moves()  # TODO Do what the docstring says


class Move:
    """A class for moving the pieces and chess notation conversions"""

    # Maps keys to values, ranks and files special chess words for same thing
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}

    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}

    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq: tuple[int, int], end_sq: tuple[int, int], board):
        """Setup all the coordinate stuff"""

        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        """Kind of like java hashcode and equals

        Simply makes a move equal regardless of how it was done, this will
        come in handy when I set up the AI"""

        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
