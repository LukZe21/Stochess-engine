import pygame
import asyncio
import sys
import copy
import re
from boards import board, piece_locations
from pieces import Pawn, Knight, Bishop, Rook, Queen, King
from chess_ai import ChessAI


def get_key_by_value(dicti, value):
    for key,val in dicti.items():
        if val == value:
            return key

piece_classes = {'pawn': Pawn, 'knight': Knight, 'bishop': Bishop, 'rook': Rook, 'queen': Queen, 'king': King}

pos_index = [["a1","a2","a3","a4","a5","a6","a7","a8"], ["b1","b2","b3","b4","b5","b6","b7","b8"], ["c1","c2","c3","c4","c5","c6","c7","c8"], ["d1","d2","d3","d4","d5","d6","d7","d8"],
    ["e1","e2","e3","e4","e5","e6","e7","e8"], ["f1","f2","f3","f4","f5","f6","f7","f8"], ["g1","g2","g3","g4","g5","g6","g7","g8"], ["h1","h2","h3","h4","h5","h6","h7","h8"]]


col_convert_dict = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7} # converting letters into numbers (In draw_pieces() function)


remaining_pieces = ['b_pawn1', 'b_pawn2', 'b_pawn3', 'b_pawn4', 'b_pawn5', 'b_pawn6', 'b_pawn7', 'b_pawn8',
                'b_knight1','b_knight2','b_bishop1','b_bishop2', 'b_rook1', 'b_rook2', 'b_queen', 'b_king'] # for ai


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


def show_moves(directions, color, moves):
    '''
    shows possible moves for selected piece
    '''
    # this if statement is needed in order to encounter the bug with pieces merging into one another.
    if moves%2==0 and color=='w' or moves%2==1 and color=='b':
        for pos in directions:
            col = col_convert_dict[pos[0]]
            row = int(pos[1])-1
            pygame.draw.rect(screen, (0, 0, 0), ((col * SQUARE_SIZE) + SQUARE_SIZE // 2 - 12, (row * SQUARE_SIZE) + SQUARE_SIZE // 2 - 12, 25, 25))




def all_piece_moves(all_white_moves=[], all_black_moves=[], board_dict=board):
    '''
    returns the two list(for black and white pieces) of all possible moves pieces are available to make.
    '''

    for key, piece in board_dict.items():
        if piece != " ":
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
                    all_white_moves = all_white_moves + possible_moves
                else:
                    all_black_moves = all_black_moves + possible_moves
    return all_white_moves, all_black_moves


moves = 0

def draw_check(piece_classes, all_white_moves, all_black_moves, cause_piece):
    try:
        cause_piece_rslt = ''.join(filter(str.isalpha, cause_piece))
        possible_block_moves = piece_classes.get(cause_piece_rslt[1:])(cause_piece, get_key_by_value(board, cause_piece), cause_piece[0]).possible_move_directions()

        white_king = 'w_king'
        pos = get_key_by_value(board, white_king)
        col, row = pos[0], int(pos[1])-1
        king_piece = piece_classes.get('king')(white_king, pos, white_king[0])

        # CHECK for white
        check = king_piece.in_checkmate(all_black_moves)
        if check:
            for move in all_white_moves:
                if move in possible_block_moves and move not in king_piece.possible_move_directions():
                    pygame.draw.rect(screen, (128,0,0), ((col_convert_dict[col] * SQUARE_SIZE) + SQUARE_SIZE // 2 - 40, (row * SQUARE_SIZE) + SQUARE_SIZE // 2 - 40, 80, 80), 4)

        black_king = 'b_king'
        pos = get_key_by_value(board, black_king)
        col, row = pos[0], int(pos[1])-1
        king_piece = piece_classes.get('king')(black_king, get_key_by_value(board, black_king), black_king[0])

        # CHECK for black
        check = king_piece.in_checkmate(all_white_moves)
        if check:
            for move in all_black_moves:
                if move in possible_block_moves and move not in king_piece.possible_move_directions():
                    pygame.draw.rect(screen, (0,0,128), ((col_convert_dict[col] * SQUARE_SIZE) + SQUARE_SIZE // 2 - 40, (row * SQUARE_SIZE) + SQUARE_SIZE // 2 - 40, 80, 80), 4)
    except:
        None
        

# main game loop
async def main():
    global moves
    global remaining_pieces
    possible_moves = []
    result1 = None
    color_piece = None

    # determines what piece user has selected
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
                if result1 != " ":
                    print(f"{first_position} : {result1}")

                if result1.startswith('w_'):
                    for piece in ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']:
                        if re.search(rf"{piece}", result1):
                            piece_class = piece_classes.get(piece)(result1, first_position, result1[0])
                            possible_moves = piece_class.possible_move_directions()
                            color_piece = result1[0] # what color is a piece

            elif event.type == pygame.MOUSEBUTTONUP:
                second_position = getPosition(mouse_x, mouse_y, pos_index) # pretty much does the same thing as above variables do.
                result2 = board.get(second_position)

                if result1.startswith('w_'):
                    if result1 != " " and (result1[0]+result2[0] != 'ww') and (result1[0]+result2[0]!='bb'): #result1 and result2 should not be same color pieces
                            if second_position in possible_moves:
                                piece_class.move(first_position, second_position)
                                possible_moves = []
                                if result2.startswith('b'):
                                    remaining_pieces.remove(result2)
                                
                                pos, best_piece = ChessAI.generate_move(remaining_pieces)
                                if pos and best_piece:
                                    print(pos, best_piece)


                                # black's generated move
                                position = get_key_by_value(board, best_piece)
                                best_piece_for_dict = ''.join(filter(str.isalpha, best_piece))
                                black_move = piece_classes.get(best_piece_for_dict[1:])(best_piece, position, 'b')
                                
                                board2 = copy.deepcopy(board)
                                black_move.move(position, pos, board_dict=board2)

                                all_white_moves, all_black_moves = all_piece_moves(board_dict=board2)

                                if not piece_classes.get('king')(f"b_king", get_key_by_value(board, f"b_king"), 'b').in_checkmate(all_white_moves):
                                    black_move.move(position, pos, board_dict=board)
                                
                                else:
                                    position = get_key_by_value(board, 'b_king')
                                    black_move = piece_classes.get('king')('b_king', position, 'b')
                                    king_moves = black_move.possible_move_directions()
                                    for move in king_moves:
                                        if move not in all_white_moves:
                                            black_move.move(position, move)
                                            break

                                # checks if piece is in checkmate or not (if it is it will quit the game)
                                # checks checkmate for black
                                if piece_classes.get('king')(f"b_king", get_key_by_value(board, f"b_king"), 'b').pos in all_white_moves:
                                    print("CHECKMATE for black")
                                    pygame.quit()
                                    sys.exit()

                                # checks checkmate for white
                                if 'w_king' in list(board.values()):  
                                    color = 'w'
                                    king_piece = piece_classes.get('king')(f"{color}_king", get_key_by_value(board, f"{color}_king"), color)
                                    checkmate = king_piece.in_checkmate(all_black_moves if result1[0]=='w' else all_white_moves)
                                    if checkmate:
                                        print("White is in check!")
                                    moves+=2
                                else:
                                    print("CHECKMATE for white")
                                    pygame.quit()
                                    sys.exit()
        
        # chessboard
        screen.blit(chessboard_img, (0,0))

        # show selected piece's moves
        show_moves(possible_moves, color_piece, moves)

        # draw existing pieces
        draw_pieces()

        # checks if piece is in check, if so it will draw square around the king in check.
        draw_check(piece_classes, all_white_moves, all_black_moves, cause_piece=result1)

        # update the display
        pygame.display.flip()

        await asyncio.sleep(0)


asyncio.run(main())