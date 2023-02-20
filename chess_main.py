"""Responsible for user input and displaying the current GameState,
basically the user's interface with the game
"""

import pygame as pg
import chess_engine

# Constants
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
FPS = 15
IMAGES = {}

def load_images() -> None:
    """Fill the IMAGES dictionary with the pieces"""

    pieces = ["wP", "bP", "wR", "bR", "wN", "bN", "wQ", "bQ", "wK", "bK"]

    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png").convert,
        (SQ_SIZE, SQ_SIZE))    

def main():
    """The main method, the actual run function"""

    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs = chess_engine.GameState()
    load_images() # Image loading is expensive so only do once
    running = True

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
        clock.tick(FPS)
        pg.display.flip()

if __name__ == "__main__":
    main()
