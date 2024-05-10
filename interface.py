import ctypes
import time
import pygame
import sys
import os
from boards import board, piece_locations

lib = ctypes.CDLL(os.path.abspath("sample.dll"))

lib.getPosition.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]
lib.getPosition.restype = ctypes.c_char_p

pos_index = [["a1","a2","a3","a4","a5","a6","a7","a8"], ["b1","b2","b3","b4","b5","b6","b7","b8"], ["c1","c2","c3","c4","c5","c6","c7","c8"], ["d1","d2","d3","d4","d5","d6","d7","d8"],
    ["e1","e2","e3","e4","e5","e6","e7","e8"], ["f1","f2","f3","f4","f5","f6","f7","f8"], ["g1","g2","g3","g4","g5","g6","g7","g8"], ["h1","h2","h3","h4","h5","h6","h7","h8"]]

flat_pos_index = [item for sublist in pos_index for item in sublist]
char_arr = (ctypes.c_char_p*len(flat_pos_index))(*[ctypes.c_char_p(item.encode()) for item in flat_pos_index])

char_ptr_arr = ctypes.cast(char_arr, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))


for key, val in piece_locations.items():
    piece_locations[key] = pygame.transform.scale(val, (80,80))

pygame.init()

WIDTH, HEIGHT = 800,800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# chessboard image
chessboard_img = pygame.image.load("imgs/chessboard.png")
chessboard_img = pygame.transform.scale(chessboard_img, (WIDTH, HEIGHT))

ROWS,COLUMNS = 8, 8

SQUARE_SIZE = HEIGHT / ROWS


def draw_pieces():
    '''
    Draws and updates the board
    '''
    for pos, val in board.items():
        col_convert_dict = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
        col = col_convert_dict[pos[0]]
        row = (int(pos[1]))-1
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
            first_position = lib.getPosition(mouse_x, mouse_y, char_ptr_arr) # what is board idx of square user has clicked on
            result1 = board.get(first_position.decode()) # what piece(or nothing) is on first_position variable
            print(f"{first_position.decode()} : {result1}")

        elif event.type == pygame.MOUSEBUTTONUP:
            second_position = lib.getPosition(mouse_x, mouse_y, char_ptr_arr) # pretty much does the same thing as above variables do.
            result2 = board.get(second_position.decode())
            if result1 != " " and (result1[0]+result2[0] != 'ww') and (result1[0]+result2[0]!='bb'): #reslt1 and and reslt2 should not be same color pieces
                # new position of result1 is on second_position variable's idx.
                new_pos = second_position.decode()
                board[new_pos] = result1

                # first_position's value will be set to " "
                key = first_position.decode()
                board[key] = " "


    # fill screen with a color
    screen.blit(chessboard_img, (0,0))
    draw_pieces()

    # update the display
    pygame.display.flip()