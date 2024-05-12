import ctypes
import pygame
import asyncio
import sys
import os
import random
import time
import re
from boards import board, piece_locations
from pieces import Pawn, Knight, Bishop, Rook, Queen, King
from chess_ai import ChessAI


# lib = ctypes.CDLL(os.path.abspath("sample.dll"))


# lib.getPosition.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]
# lib.getPosition.restype = ctypes.c_char_p


def get_key_by_value(dicti, value):
    for key,val in dicti.items():
        if val == value:
            return key


pos_index = [["a1","a2","a3","a4","a5","a6","a7","a8"], ["b1","b2","b3","b4","b5","b6","b7","b8"], ["c1","c2","c3","c4","c5","c6","c7","c8"], ["d1","d2","d3","d4","d5","d6","d7","d8"],
    ["e1","e2","e3","e4","e5","e6","e7","e8"], ["f1","f2","f3","f4","f5","f6","f7","f8"], ["g1","g2","g3","g4","g5","g6","g7","g8"], ["h1","h2","h3","h4","h5","h6","h7","h8"]]


col_convert_dict = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7} # converting letters into numbers (In draw_pieces() function)

possible_moves = [] # possible moves of pieces
possible_moves_ai = [] # possible moves of pieces (ai)


remaining_pieces = ['b_pawn1', 'b_pawn2', 'b_pawn3', 'b_pawn4', 'b_pawn5', 'b_pawn6', 'b_pawn7', 'b_pawn8',
                    'b_knight1','b_knight2','b_bishop1','b_bishop2', 'b_rook1', 'b_rook2', 'b_queen', 'b_king'] # for ai

# flat_pos_index = [item for sublist in pos_index for item in sublist]
# char_arr = (ctypes.c_char_p*len(flat_pos_index))(*[ctypes.c_char_p(item.encode()) for item in flat_pos_index])

# char_ptr_arr = ctypes.cast(char_arr, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))


# resizing chess pieces
for key, val in piece_locations.items():
    piece_locations[key] = pygame.transform.scale(val, (80,80))

def getPosition(mouseX, mouseY, pos_index):
    return pos_index[mouseX//100][mouseY//100]


pygame.init()
# pygame.mixer.init()

WIDTH, HEIGHT = 800,800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# chessboard image
chessboard_img = pygame.image.load("imgs/chessboard.png")
chessboard_img = pygame.transform.scale(chessboard_img, (WIDTH, HEIGHT))

# piece move icon
move_icon_img = pygame.image.load("imgs/move_icon.png")
move_icon_img = pygame.transform.scale(move_icon_img, (80,80))

# sounds
# piece_move = pygame.mixer.Sound('sounds/piece_move.mp3')
# piece_capture = pygame.mixer.Sound('sounds/piece_capture.mp3')


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



def all_piece_moves(all_white_moves=[], all_black_moves=[]):
    '''
    returns the two list(for black and white pieces) of all possible moves pieces are available to make.
    '''
    pieces = ['w_pawn1','w_pawn2','w_pawn3','w_pawn4','w_pawn5','w_pawn6','w_pawn7','w_pawn8'
              'w_knight1','w_knight2', 'w_bishop1', 'w_bishop2','w_rook1','w_rook2', 'w_queen', 'w_king',
              'b_pawn1','b_pawn2','b_pawn3','b_pawn4','b_pawn5','b_pawn6','b_pawn7','b_pawn8'
              'b_knight1','b_knight2', 'b_bishop1', 'b_bishop2','b_rook1','b_rook2', 'b_queen', 'b_king']
    piece_classes = {'pawn': Pawn, 'knight': Knight, 'bishop': Bishop, 'rook': Rook, 'queen': Queen, 'king': King}

    for key, value in board.items():
        for piece in pieces:
            if piece == value:
                if piece[2:] not in ['queen', 'king']:
                    piece_class = piece_classes.get(piece[2:-1])(piece, key, piece[0])
                    possible_moves = piece_class.possible_move_directions()
                    if piece[0] == 'w':
                        all_white_moves = all_white_moves+possible_moves
                    else:
                        all_black_moves = all_black_moves+possible_moves
                elif piece[2:] in ['queen', 'king']:
                    piece_class = piece_classes.get(piece[2:])(piece, key, piece[0])
                    possible_moves = piece_class.possible_move_directions()
                    if piece[0] == 'w':
                        all_white_moves = all_white_moves+possible_moves
                    else:
                        all_black_moves = all_black_moves+possible_moves
    return all_white_moves, all_black_moves


check_count = 0
# main game loop
async def main():
    global check_count
    possible_moves = []
    result1 = None
    while True:
        for event in pygame.event.get():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            all_white_moves, all_black_moves = all_piece_moves()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    first_position = getPosition(mouse_x, mouse_y, pos_index) # what is board idx of square user has clicked on
                    result1 = board.get(first_position) # what piece(or nothing) is on first_position variable
                    print(f"{first_position} : {result1}")

                    # determines what piece user has selected
                    piece_classes = {'pawn': Pawn, 'knight': Knight, 'bishop': Bishop, 'rook': Rook, 'queen': Queen, 'king': King}
                    if result1.startswith('w_'):
                        for piece in ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']:
                            if re.search(rf"{piece}", result1):
                                piece_class = piece_classes.get(piece)(result1, first_position, result1[0])
                                possible_moves = piece_class.possible_move_directions()

                            # generated moves
                            possible_moves_ai = []
                            while possible_moves_ai == []:
                                result1_ai = ChessAI.generate_move(remaining_pieces)
                                for key, val in board.items():
                                    if val == result1_ai:
                                        first_position_ai = key
                                for piece_ai in ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']:
                                    if re.search(rf"{piece_ai}", result1_ai):
                                        piece_class_ai = piece_classes.get(piece_ai)(result1_ai, first_position_ai, result1_ai[0])
                                        possible_moves_ai = piece_class_ai.possible_move_directions()
                            piece_class_ai_king = piece_classes.get('king')('b_king', get_key_by_value(board, 'b_king'), 'b')
                            if piece_class_ai_king.is_check(all_white_moves):
                                print("CHECKK")
                                first_position_ai = get_key_by_value(board, 'b_king')
                                piece_class_ai = piece_class_ai_king
                                possible_moves_ai = piece_class_ai_king.possible_move_directions()


            elif event.type == pygame.MOUSEBUTTONUP:
                second_position = getPosition(mouse_x, mouse_y, pos_index) # pretty much does the same thing as above variables do.
                result2 = board.get(second_position)
                if result1.startswith('w_'):
                    if result1 != " " and (result1[0]+result2[0] != 'ww') and (result1[0]+result2[0]!='bb'): #result1 and result2 should not be same color pieces
                        if second_position in possible_moves:
                            piece_class.move(first_position, second_position)
                            possible_moves = []

                            if possible_moves_ai != []:
                                move = random.choice(possible_moves_ai)
                                piece_class_ai.move(first_position_ai, move)
                                possible_moves_ai = []
                for king in ['w_king', 'b_king']:
                    king_piece = piece_classes.get('king')(king, get_key_by_value(board, king), king[0])
                        
                    # CHECK
                    check = king_piece.is_check(all_white_moves if king=='b_king' else all_black_moves)
                    if check:
                        if check_count > 1:
                            print(f"{'White' if king[0]=='b' else 'Black'} WON!")
                        check_count += 1
 
            
        # chessboard
        screen.blit(chessboard_img, (0,0))

        # show selected piece's moves
        show_moves(possible_moves)

        # draw existing pieces
        draw_pieces()

        # update the display
        pygame.display.flip()

        # checks checkmate for opposite color of selected piece.   
                # # CHECKMATE
                # checkmate = king_piece.is_checkmate(all_white_moves if king=='b_king' else all_black_moves)
                # if checkmate:
                #     print("GAME OVER")
                #     time.sleep(10)
                #     pygame.quit()
                #     sys.exit()


        
        await asyncio.sleep(0)


asyncio.run(main())