import ctypes
import time
import pygame
import sys
import os

lib = ctypes.CDLL(os.path.abspath("sample.dll"))

lib.getMoves.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
lib.getMoves.restype = ctypes.c_char_p

white_pieces_location = [100, 100]
int_array = (ctypes.c_int * len(white_pieces_location))(*white_pieces_location)

board = [[{"b_rook1": "a8","b_knight1": "b8", "b_bishop1": "c8","b_queen": "d8","b_king": "e8","b_bishop2": "f8","b_knight2": "g8","b_rook2": "h8"}],
         [{"b_pawn1": "a7","b_pawn2": "b7", "b_pawn3": "c7","b_pawn4": "d7", "b_pawn5": "e7","b_pawn6": "f7","b_pawn7": "g7","b_pawn8": "h7"}],
         [{" ": "a6"," ": "b6", " ": "c6"," ": "d6"," ": "e6"," ": "f6"," ": "g6"," ": "h6"}],
         [{" ": "a5"," ": "b5", " ": "c5"," ": "d5"," ": "e5"," ": "f5"," ": "g5"," ": "h5"}],
         [{" ": "a4"," ": "b4", " ": "c4"," ": "d4"," ": "e4"," ": "f4"," ": "g4"," ": "h4"}],
         [{" ": "a3"," ": "b3", " ": "c3"," ": "d3"," ": "e3"," ": "f3"," ": "g3"," ": "h3"}],
         [{"w_pawn1": "a2","w_pawn2": "b2", "w_pawn3": "c2","w_pawn3": "d2", "w_pawn3": "e2","w_pawn3": "f2","w_pawn3": "g2","w_pawn3": "h2"}],
         [{"w_rook1": "a1","w_knight1": "b1", "w_bishop1": "c1","w_queen": "d1","w_king": "e1","w_bishop2": "f1","w_knight2": "g1","w_rook2": "h1"}]]


class Piece:
    def __init__(self, unique_name, position):
        self.unique_name = unique_name
        self.position = position

        def Move(self, new_position):
            position = new_position
            return position



bishop_black = pygame.image.load("Pieces/bishop_black.png")
knight_black = pygame.image.load("Pieces/knight_black.png")
queen_black = pygame.image.load("Pieces/queen_black.png")
king_black = pygame.image.load("Pieces/king_black.png")
rook_black = pygame.image.load("Pieces/rook_black.png")
pawn_black = pygame.image.load("Pieces/pawn_black.png")

bishop_white = pygame.image.load("Pieces/bishop_white.png")
knight_white = pygame.image.load("Pieces/knight_white.png")
queen_white = pygame.image.load("Pieces/queen_white.png")
king_white = pygame.image.load("Pieces/king_white.png")
rook_white = pygame.image.load("Pieces/rook_white.png")
pawn_white = pygame.image.load("Pieces/pawn_white.png")


piece_locations = [[[rook_white, knight_white, bishop_white, queen_white, king_white, bishop_white, knight_white, rook_white],
                   [pawn_white, pawn_white, pawn_white, pawn_white, pawn_white, pawn_white, pawn_white, pawn_white]], [[rook_black, knight_black, bishop_black,
                    queen_black, king_black, bishop_black, knight_black, rook_black],
                   [pawn_black, pawn_black, pawn_black, pawn_black, pawn_black, pawn_black, pawn_black, pawn_black]]]

for color_side in piece_locations:
    for row in color_side:
        for piece_idx in range(len(row)):
            row[piece_idx] = pygame.transform.scale(row[piece_idx], (80,80))

pygame.init()

WIDTH, HEIGHT = 800,800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# chessboard image
chessboard_img = pygame.image.load("chessboard.png")
chessboard_img = pygame.transform.scale(chessboard_img, (WIDTH, HEIGHT))

ROWS,COLUMNS = 8,8

SQUARE_SIZE = HEIGHT / ROWS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



white_pieces_location = [(0, 100), (100, 200), (200, 300), (400, 500), (500, 600),
                         (600, 700), (700,800)]

def draw_pieces():
    PIECE_SIZE = SQUARE_SIZE // 2
    for row in range(ROWS):
        i = 0
        for col in range(COLUMNS):
            # if(row+col)%2 !=0:
            #     continue
            if row == 0:
                screen.blit(piece_locations[0][0][i], (col*SQUARE_SIZE+SQUARE_SIZE//2-40, row*SQUARE_SIZE+SQUARE_SIZE//2-40))
                i+=1
            elif row == 1:
                screen.blit(piece_locations[0][1][i], (col*SQUARE_SIZE+SQUARE_SIZE//2-40, row*SQUARE_SIZE+SQUARE_SIZE//2-40))
                i+=1
            elif row == 6:
                screen.blit(piece_locations[1][1][i], (col*SQUARE_SIZE+SQUARE_SIZE//2-40, row*SQUARE_SIZE+SQUARE_SIZE//2-40))
                i+=1
            elif row == 7:
                screen.blit(piece_locations[1][0][i], (col*SQUARE_SIZE+SQUARE_SIZE//2-40, row*SQUARE_SIZE+SQUARE_SIZE//2-40))
                i+=1


# main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            result = lib.getMoves(mouse_x, mouse_y, int_array, len(white_pieces_location))
            print(result.decode())
            print((mouse_x, mouse_y))

    # fill screen with a color
    screen.blit(chessboard_img, (0,0))
    draw_pieces()

    # update the display
    pygame.display.flip()