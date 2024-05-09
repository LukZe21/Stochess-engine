import ctypes
import time
import pygame
import sys
import os

lib = ctypes.CDLL(os.path.abspath("sample.dll"))

lib.getPosition.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]
lib.getPosition.restype = ctypes.c_char_p

pos_index = [["a8","a7","a6","a5","a4","a3","a2","a1"], ["b8","b7","b6","b5","b4","b3","b2","b1"], ["c8","c7","c6","c5","c4","c3","c2","c1"], ["d8","d7","d6","d5","d4","d3","d2","d1"],
             ["e8","e7","e6","e5","e4","e3","e2","e1"], ["f8","f7","f6","f5","f4","f3","f2","f1"], ["g8","g7","g6","g5","g4","g3","g2","g1"], ["h8","h7","h6","h5","h4","h3","h2","h1"]]

flat_pos_index = [item for sublist in pos_index for item in sublist]
char_arr = (ctypes.c_char_p*len(flat_pos_index))(*[ctypes.c_char_p(item.encode()) for item in flat_pos_index])

char_ptr_arr = ctypes.cast(char_arr, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))

board = {"a8": "b_rook1", "b8": "b_knight1", "c8": "b_bishop1", "d8": "b_queen", "e8": "b_king", "f8": "b_bishop2", "g8": "b_knight2", "h8": "b_rook2",
         "a7": "b_pawn1", "b7": "b_pawn2", "c7": "b_pawn3", "d7": "b_pawn4", "e7": "b_pawn5", "f7": "b_pawn6", "g7": "b_pawn7", "h7": "b_pawn8",
         "a6": " ", "b6": " ", "c6": " ", "d6": " ", "e6": " ", "f6": " ", "g6": " ", "h6": " ",
         "a5": " ", "b5": " ", "c5": " ", "d5": " ", "e5": " ", "f5": " ", "g5": " ", "h5": " ",
         "a4": " ", "b4": " ", "c4": " ", "d4": " ", "e4": " ", "f4": " ", "g4": " ", "h4": " ",
         "a3": " ", "b3": " ", "c3": " ", "d3": " ", "e3": " ", "f3": " ", "g3": " ", "h3": " ",
         "a2": "w_pawn1", "b2": "w_pawn2", "c2": "w_pawn3", "d2": "w_pawn4", "e2": "w_pawn5", "f2": "w_pawn6", "g2": "w_pawn7", "h2": "w_pawn8",
         "a1": "w_rook1", "b1": "w_knight1", "c1": "w_bishop1", "d1": "w_queen", "e1": "w_king", "f1": "w_bishop2", "g1": "w_knight2", "h1": "w_rook2"}



class Piece:
    def __init__(self, unique_name, position):
        self.unique_name = unique_name
        self.position = position

        def Move(self, new_position):
            position = new_position
            return position
        

def position_of_piece(position, board):
    for key, val in board.items():
        if key == position and val != " ":
            return val
    return "None"

def move_piece(position1, position2, mouse_x, mouse_y):
    position2_val = position_of_piece(position2, board)
    if board.get(position1) != " " and position2_val == "None":
        new_pos = lib.getPosition(mouse_x, mouse_y, char_ptr_arr)
        return new_pos.decode()

def get_key_by_value(dicti, value):
    for key,val in dicti.items():
        if val == value:
            return key



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


piece_locations = {"b_rook1": rook_white,"b_knight1": knight_white,"b_bishop1": bishop_white,"b_queen": queen_white,
                    "b_king": king_white,"b_bishop2": bishop_white,"b_knight2": knight_white,"b_rook2": rook_white,
                    "b_pawn1": pawn_white, "b_pawn2":pawn_white, "b_pawn3":pawn_white, "b_pawn4":pawn_white, "b_pawn5":pawn_white,
                    "b_pawn6":pawn_white,"b_pawn7": pawn_white,"b_pawn8": pawn_white,           
                    "w_rook1": rook_black,"w_knight1":knight_black, "w_bishop1": bishop_black, "w_queen":queen_black,
                    "w_king": king_black,"w_bishop2": bishop_black, "w_knight2": knight_black, "w_rook2": rook_black,
                   "w_pawn1":pawn_black, "w_pawn2":pawn_black, "w_pawn3":pawn_black, "w_pawn4":pawn_black, "w_pawn5":pawn_black,
                   "w_pawn6":pawn_black, "w_pawn7":pawn_black, "w_pawn8":pawn_black}


for key, val in piece_locations.items():
    piece_locations[key] = pygame.transform.scale(val, (80,80))

pygame.init()

WIDTH, HEIGHT = 800,800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# chessboard image
chessboard_img = pygame.image.load("chessboard.png")
chessboard_img = pygame.transform.scale(chessboard_img, (WIDTH, HEIGHT))

ROWS,COLUMNS = 8, 8

SQUARE_SIZE = HEIGHT / ROWS


def draw_pieces():
    for pos, val in board.items():
        col_convert_dict = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
        col = col_convert_dict[pos[0]]
        row = ((int(pos[1]))-1)
        # print(row, col)
        if val != " ":
            screen.blit(piece_locations.get(val), ((col)*SQUARE_SIZE+SQUARE_SIZE//2-40, (row)*SQUARE_SIZE+SQUARE_SIZE//2-40))


# main game loop
while True:
    for event in pygame.event.get():
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            position1 = lib.getPosition(mouse_x, mouse_y, char_ptr_arr)
            result1 = position_of_piece(position1.decode(), board)
            print(f"{position1.decode()} : {result1}")
        elif event.type == pygame.MOUSEBUTTONUP:
            position2 = lib.getPosition(mouse_x, mouse_y, char_ptr_arr)
            result2 = position_of_piece(position2.decode(), board)
            new_pos = move_piece(position1.decode(), position2.decode(), mouse_x, mouse_y)
            print(new_pos)
            key = get_key_by_value(board, result1)
            board[new_pos] = result1
            print(board[new_pos])
            board[key] = " "


    # fill screen with a color
    screen.blit(chessboard_img, (0,0))
    draw_pieces()

    # update the display
    pygame.display.flip()