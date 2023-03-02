"""Responsible for user input and displaying the current GameState,
basically the user's interface with the game
"""
# Imports
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

    pieces = ["wP", "bP", "wR", "bR", "wN", "bN", "wB", "bB", "wQ", "bQ", "wK", "bK"]

    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"),
                                           (SQ_SIZE, SQ_SIZE))


def draw_gamestate(screen: pg.Surface, gs: chess_engine.GameState) -> None:
    """Draw onto the screen the entire current game"""

    draw_board(screen)  # draw the chessboard
    draw_pieces(screen, gs.board)  # draw the chess pieces on the board


def draw_board(screen: pg.Surface) -> None:
    """Draw the squares of the board onto the screen
    
    The light squares will be even, 0 is even, and the dark squares are all odd,
    so just need to modulo 2 to check if a square is odd or even and then colour it in
    """

    colours = [pg.Color("white"), pg.Color("gray")]  # TODO make this configurable
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            colour = colours[((i + j) % 2)]
            pg.draw.rect(screen, colour, pg.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen: pg.Surface, board) -> None:
    """Draw the pieces onto the board"""

    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def main() -> None:
    """The main method, the actual runnable function"""

    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Chess")
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs = chess_engine.GameState()
    valid_moves: list = gs.check_moves()
    move_made: bool = False
    load_images()  # Image loading is expensive so only do once
    running: bool = True
    sq_selected = ()  # Keeps track of the last click
    player_clicks = []  # Keeps track of the last clicks

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            # Mouse input handling
            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):  # Same square, deselect
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2:
                    move = chess_engine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                    sq_selected = ()  # Reset
                    player_clicks = []  # Reset
            # Keyboard input handling
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:  # Z is undo button
                    gs.undo_move()
                    move_made = True

        if move_made:
            valid_moves = gs.check_moves()
            move_made = False
        draw_gamestate(screen, gs)
        clock.tick(FPS)
        pg.display.flip()


if __name__ == "__main__":
    main()
