"""
Responsible for storing the current game's information,
for determining valid moves for the current state and a history of the moves taken
"""
# Imports
import numpy as np


class GameState:
    """
    The game state class.
    """

    def __init__(self):
        """
        Sets up the board, whose move it is and a move log.

        Sets up the board as a 8x8 Numpy 2d array. Each piece is represented by 2 characters,
        the first character represents the colour, second character represents piece:
        R = Rook, N = Knight, B = Bishop, Q = Queen and K = King. -- represents empty space.
        :return:
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

        self.move_functions = {
            "P": self.pawn_move,
            "R": self.rook_move,
            "N": self.knight_move,
            "B": self.bishop_move,
            "Q": self.queen_move,
            "K": self.king_move
        }

        # Who's turn
        self.white_to_move: bool = True

        self.movelog: list = []

        # King pieces' locations
        self.white_king_loc = (7, 4)
        self.black_king_loc = (0, 4)

    def make_move(self, move):
        """
        The method that actual moves the pieces on the board, doesn't work for special moves like castling

        :param move: The move that needs to be made.
        :return:
        """

        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.movelog.append(move)  # Add to log
        self.white_to_move = not self.white_to_move  # Swap turn
        # Update the king's location if it was moved
        if move.piece_moved == "wK":
            self.white_king_loc = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_loc = (move.end_row, move.end_col)

    def undo_move(self):
        """
        Undoes the move.

        :return:
        """
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            # Update the king's location
            if move.piece_moved == "wK":
                self.white_king_loc = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_loc = (move.start_row, move.start_col)

    def valid_moves(self):
        """
        All the possible moves, with checking for check.

        :return: The array holding the moves made.
        """
        moves = self.all_moves()
        for i in range(len(moves) - 1, -1, -1):  # going back through the list
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()
        return moves

    def in_check(self):
        """
        Checks if the current player king is in check.

        :return: Whether the square the king is on is attacked or not.
        """

        if self.white_to_move:
            return self.square_attacked(self.white_king_loc[0], self.white_king_loc[1])
        else:
            return self.square_attacked(self.black_king_loc[0], self.black_king_loc[1])

    def square_attacked(self, r: int, c: int):
        """
        Checks if the enemy can attack square r, c.

        :param r: The row number of the square
        :param c: The column number of the square
        :return: Whether a particular square is under attack or not.
        """

        self.white_to_move = not self.white_to_move  # Switch turn (temporary)
        opp_moves = self.all_moves()
        self.white_to_move = not self.white_to_move  # Switch back
        for move in opp_moves:
            if move.end_row == r and move.end_col == c:  # Square is under attack
                return True
        return False

    def all_moves(self):
        """
        All the possible moves, without checking for check.

        :return: The array holding the moves made.
        """

        moves = []  # The array holding all the moves done
        for r in range(len(self.board)):  # Rows
            for c in range(len(self.board[r])):  # Cols
                turn = self.board[r][c][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)

        return moves

    def pawn_move(self, r: int, c: int, moves: list):
        """
        The valid moves a pawn can make.

        :param r: The number representing the row.
        :param c: The number representing the column.
        :param moves: The array holding all the moves.
        :return:
        """

        if self.white_to_move:  # Checks its white's turn to move
            if self.board[r - 1][c] == "--":  # Checks square in front is empty
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 6 to check it is he first move
                    moves.append(Move((r, c), (r - 2, c), self.board))

            if c - 1 >= 0:  # Capturing diagonally to the left
                if self.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))

            if c + 1 <= 7:  # Capturing diagonally to the right
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # Black's turn to move
            if self.board[r + 1][c] == "--":  # Checks square is empty
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))

            if c - 1 >= 0:  # Capturing diagonally to the left
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))

            if c + 1 <= 7:  # Capturing diagonally to the right
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def rook_move(self, r: int, c: int, moves: list):
        """
        The valid moves a rook can make.

        :param r: The number representing the row.
        :param c: The number representing the column.
        :param moves: The array holding all the moves.
        :return:
        """

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # cardinal directions
        enemy_colour = "b" if self.white_to_move else "w"

        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # empty space ok
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_colour:  # enemy ok
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:  # own team not ok
                        break
                else:  # off board not ok
                    break

    def knight_move(self, r: int, c: int, moves: list):
        """
        The valid moves a knight can make

        :param r: The number representing the row.
        :param c: The number representing the column.
        :param moves: The array holding all the moves.
        :return:
        """

        knight_moves = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2))
        ally_colour = "w" if self.white_to_move else "b"

        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_colour:
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    def bishop_move(self, r: int, c: int, moves: list):
        """
        The valid moves a bishop can make

        :param r: The number representing the row.
        :param c: The number representing the column.
        :param moves: The array holding all the moves.
        :return:
        """

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_colour = "b" if self.white_to_move else "w"

        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_colour:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def queen_move(self, r: int, c: int, moves: list):
        """
        The valid moves a queen can make

        :param r: The number representing the row.
        :param c: The number representing the column.
        :param moves: The array holding all the moves.
        :return:
        """

        self.rook_move(r, c, moves)
        self.bishop_move(r, c, moves)  # queen is basically just rook + bishop

    def king_move(self, r: int, c: int, moves: list):
        """
        The valid moves a king can make

        :param r: The number representing the row.
        :param c: The number representing the column.
        :param moves: The array holding all the moves.
        :return:
        """

        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_colour = "w" if self.white_to_move else "b"

        for i in range(8):
            end_row = r + king_moves[i][0]
            end_col = c + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_colour:
                    moves.append(Move((r, c), (end_row, end_col), self.board))


class Move:
    """
    A class for moving the pieces and chess notation conversions
    """

    # Maps keys to values, ranks and files special chess words for same thing
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}

    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}

    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq: tuple[int, int], end_sq: tuple[int, int], board):
        """
        Setting up the coordinate system.

        :param start_sq: The starting square (row and column).
        :param end_sq: The ending square (row and column).
        :param board: The chessboard.
        """

        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        """
        Kind of like Java hashcode and equals.

        Simply makes a move equal regardless of how it was done, this will
        come in handy when I set up the AI.

        :param other: The other object I am comparing to.
        :return: Returns true if they are equal and returns false otherwise.
        """

        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        """
        Just gets the chess notation, or close to it, of a move.

        :return:
        """
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        """
        An intermediary function for getting chess notation working.

        :param r: The row.
        :param c: The column.
        :return: Nothing to see here, never use this directly.
        """
        return self.cols_to_files[c] + self.rows_to_ranks[r]
