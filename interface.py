import ctypes
import time
import pygame
import sys
import os
import re
from boards import board, piece_locations

lib = ctypes.CDLL(os.path.abspath("sample.dll"))

lib.getPosition.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]
lib.getPosition.restype = ctypes.c_char_p

pos_index = [["a1","a2","a3","a4","a5","a6","a7","a8"], ["b1","b2","b3","b4","b5","b6","b7","b8"], ["c1","c2","c3","c4","c5","c6","c7","c8"], ["d1","d2","d3","d4","d5","d6","d7","d8"],
    ["e1","e2","e3","e4","e5","e6","e7","e8"], ["f1","f2","f3","f4","f5","f6","f7","f8"], ["g1","g2","g3","g4","g5","g6","g7","g8"], ["h1","h2","h3","h4","h5","h6","h7","h8"]]


col_convert_dict = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7} # converting letters into numbers (In draw_pieces() function)

possible_moves = [] # possible moves of pieces

flat_pos_index = [item for sublist in pos_index for item in sublist]
char_arr = (ctypes.c_char_p*len(flat_pos_index))(*[ctypes.c_char_p(item.encode()) for item in flat_pos_index])

char_ptr_arr = ctypes.cast(char_arr, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))


# resizing chess pieces
for key, val in piece_locations.items():
    piece_locations[key] = pygame.transform.scale(val, (80,80))


class Piece:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

    def move(self, pos1, pos2):
        pos1 = pos1
        pos2 = pos2
        if result1 != " " and (board.get(pos1)[0]+board.get(pos2)[0] != 'ww') and (board.get(pos1)[0]+board.get(pos2)[0]!='bb'):
            board[pos1] = " "
            board[pos2] = self.name


def get_key_by_value(dicti, value):
    for key,val in dicti.items():
        if val == value:
            return key


class Pawn(Piece):
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

    def possible_move_directions(self, color):
        col_letters = ['h','g','f','e','d','c','b','a']
        # solid moves
        col, row = self.pos[0], int(self.pos[1])
        possible_moves = []
        number_of_moves = (3 if self.pos in ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'] else 2) if color == 'w' else (3 if self.pos in ['a2','b2','c2','d2','e2','f2','g2','h2'] else 2)
        for i in range(1, number_of_moves):
            move_position = f"{col}{row-i}" if color == 'w' else f"{col}{row+i}"
            if board[move_position] == " ":
                possible_moves.append(move_position)

        # attack moves
        col, row = self.pos[0], int(self.pos[1])
        possible_move_attacks = []
        for idx, i in enumerate(col_letters):
            if col == i:
                attack_position = f"{col_letters[idx-1]}{row-1}" if color == 'w' else f"{col_letters[idx-1]}{row+1}"
                if (board[attack_position].startswith('b_') and color == 'w') or (board[attack_position].startswith('w_') and color == 'b'):
                    possible_move_attacks.append(attack_position)
        return possible_moves + possible_move_attacks





pygame.init()

WIDTH, HEIGHT = 800,800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# chessboard image
chessboard_img = pygame.image.load("imgs/chessboard.png")
chessboard_img = pygame.transform.scale(chessboard_img, (WIDTH, HEIGHT))

# piece move icon
move_icon_img = pygame.image.load("imgs/move_icon.png")
move_icon_img = pygame.transform.scale(move_icon_img, (80,80))


ROWS,COLUMNS = 8, 8

SQUARE_SIZE = HEIGHT / ROWS


def draw_pieces():
    '''
    Draws and updates the board
    '''
    for pos, val in board.items():
        col = col_convert_dict[pos[0]]
        row = (int(pos[1]))-1
        # print(row, col)
        if val != " ":
            screen.blit(piece_locations.get(val), ((col)*SQUARE_SIZE+SQUARE_SIZE//2-40, (row)*SQUARE_SIZE+SQUARE_SIZE//2-40))


def show_moves(directions):
    '''
    shows possible moves for selected piece
    '''
    for pos in directions:
        col = col_convert_dict[pos[0]]
        row = int(pos[1])-1
        screen.blit(move_icon_img, ((col)*SQUARE_SIZE+SQUARE_SIZE//2-40, (row)*SQUARE_SIZE+SQUARE_SIZE//2-40))


# main game loop
while True:
    for event in pygame.event.get():
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            first_position = lib.getPosition(mouse_x, mouse_y, char_ptr_arr).decode() # what is board idx of square user has clicked on
            result1 = board.get(first_position) # what piece(or nothing) is on first_position variable
            print(f"{first_position} : {result1}")

            if re.search(r'pawn', result1):
                pawn = Pawn(result1, first_position)
                possible_moves = pawn.possible_move_directions(result1[0])

        elif event.type == pygame.MOUSEBUTTONUP:
            second_position = lib.getPosition(mouse_x, mouse_y, char_ptr_arr).decode() # pretty much does the same thing as above variables do.
            result2 = board.get(second_position)

            if result1 != " " and (result1[0]+result2[0] != 'ww') and (result1[0]+result2[0]!='bb'): #reslt1 and and reslt2 should not be same color pieces
                    if second_position in possible_moves:
                        pawn.move(first_position, second_position)
                        possible_moves = []
                # new_pos = second_position.decode()
                # board[new_pos] = result1

                # # first_position's value will be set to " "
                # key = first_position.decode()
                # board[key] = " "


    # fill screen with a color
    screen.blit(chessboard_img, (0,0))
    show_moves(possible_moves)
    draw_pieces()

    # update the display
    pygame.display.flip()