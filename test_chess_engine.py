import unittest
import chess_engine
import numpy as np

class TestChessEngine(unittest.TestCase):
    """This class will be testing the engine first
    
    First three tests check that the engine initialised correctly
    """

    def setUp(self):
        self.gs = chess_engine.GameState()


    def test_board(self):
        self.assertTrue((self.gs.board==np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ])).all())


    def test_white_first(self):
        self.assertTrue(self.gs.white_to_move)    


    def test_movelog_empty(self):
        self.assertEqual(self.gs.movelog, [])

if __name__ == "__main__":
    unittest.main()