import pygame
import asyncio
import sys
import copy
import re
from boards import board, piece_locations
from pieces import Pawn, Knight, Bishop, Rook, Queen, King
from chess_ai import ChessAI
from stockfishBot import start_stockfish, set_skill_level, stockfish_move


def get_key_by_value(dicti, value):
    for key,val in dicti.items():
        if val == value:
            return key

piece_classes = {'pawn': Pawn, 'knight': Knight, 'bishop': Bishop, 'rook': Rook, 'queen': Queen, 'king': King}

pos_index = [["a1","a2","a3","a4","a5","a6","a7","a8"], ["b1","b2","b3","b4","b5","b6","b7","b8"], ["c1","c2","c3","c4","c5","c6","c7","c8"], ["d1","d2","d3","d4","d5","d6","d7","d8"],
    ["e1","e2","e3","e4","e5","e6","e7","e8"], ["f1","f2","f3","f4","f5","f6","f7","f8"], ["g1","g2","g3","g4","g5","g6","g7","g8"], ["h1","h2","h3","h4","h5","h6","h7","h8"]]


col_convert_dict = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7} # converting letters into numbers (In draw_pieces() function)


moves = 1 # how many moves has been made (is being used to determine which side's turn it is)


# resizing chess pieces
for key, val in piece_locations.items():
    piece_locations[key] = pygame.transform.scale(val, (80,80))

def getPosition(mouseX, mouseY, pos_index):
    return pos_index[mouseX//100][mouseY//100]


pygame.init()
# pygame.mixer.init()

WIDTH, HEIGHT = 800,800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Chess")

# chessboard image
chessboard_img = pygame.image.load("imgs/chessboard1.png")
chessboard_img = pygame.transform.scale(chessboard_img, (WIDTH, HEIGHT))


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
        try:
            col = col_convert_dict[pos[0]]
            row = (int(pos[1]))-1
            if val != " ":
                screen.blit(piece_locations.get(val), ((col)*SQUARE_SIZE+SQUARE_SIZE//2-40, (row)*SQUARE_SIZE+SQUARE_SIZE//2-40))
        except:
            continue


def show_moves(directions, color, moves, mouseX, mouseY):
    '''
    shows possible moves for selected piece
    '''
    # this if statement is needed in order to encounter the bug with pieces merging into one another.
    if moves%2==0 and color=='w' or moves%2==1 and color=='b':
        position_of_piece = getPosition(mouseX, mouseY, pos_index)
        col = col_convert_dict[position_of_piece[0]]
        row = int(position_of_piece[1])-1
        pygame.draw.rect(screen, (209, 250, 47), ((col * SQUARE_SIZE), (row * SQUARE_SIZE) + 1, 100, 101))
        # selected_piece = pygame.Surface((100,101))
        # selected_piece.set_alpha(200)
        # selected_piece.fill((209, 250, 47))
        # screen.blit(selected_piece, ((col*SQUARE_SIZE), (row*SQUARE_SIZE)+1))

        for pos in directions:
            col = col_convert_dict[pos[0]]
            row = int(pos[1])-1
            if board.get(pos).startswith('b_'):
                pygame.draw.circle(screen, (245, 66, 66), ((col * SQUARE_SIZE) + SQUARE_SIZE // 2, (row * SQUARE_SIZE) + SQUARE_SIZE // 2), 45, width=5)
            else:
                pygame.draw.circle(screen, (219, 219, 219), ((col * SQUARE_SIZE) + SQUARE_SIZE // 2, (row * SQUARE_SIZE) + SQUARE_SIZE // 2), 25)




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




def draw_check(piece_classes, all_white_moves, all_black_moves, cause_piece):
    """ Draws square around the king piece that is in check. """
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



# starts and sets skill level for stockfish chess bot
start_stockfish()
set_skill_level(20)

# main game loop
async def main():
    global moves
    possible_moves = []
    result1 = None
    color_piece = None
    selected_piece_posX, selected_piece_posY = None, None
    moves_lst = []
    down = False

    # determines what piece user has selected
    while True:
        # if it is white's turn stockfish will make a move.
        if moves%2==1:
            stockfish_move(moves_lst, board)
            moves+=1      

        for event in pygame.event.get():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            all_white_moves, all_black_moves = all_piece_moves()
             

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            elif event.type == pygame.MOUSEBUTTONDOWN:
                # for click move
                prev_location = get_key_by_value(board, result1)

                # Drag and Drop move
                first_position = getPosition(mouse_x, mouse_y, pos_index) # what is board idx of square user has clicked on
                result1 = board.get(first_position) # what piece(or nothing) is on first_position variable

                down = True # makes down variable true for dragging selected piece.

                if result1 != " ":
                    print(f"{first_position} : {result1}")

                if result1.startswith('w_'):
                    selected_piece_posX, selected_piece_posY = mouse_x, mouse_y
                    for piece in ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']:
                        if re.search(rf"{piece}", result1):
                            piece_class = piece_classes.get(piece)(result1, first_position, result1[0])
                            possible_moves = piece_class.possible_move_directions()
                            color_piece = result1[0] # what color is a piece

            elif event.type == pygame.MOUSEBUTTONUP:
                
                # Drag and Drop move
                second_position = getPosition(mouse_x, mouse_y, pos_index) # pretty much does the same thing as above variables do.
                result2 = board.get(second_position)

                if result1.startswith('w_') and moves%2==0:
                    if result1 != " " and (result1[0]+result2[0] != 'ww') and (result1[0]+result2[0]!='bb'): #result1 and result2 should not be same color pieces
                            if second_position in possible_moves:
                                piece_class.move(first_position, second_position)
                                moves_lst.append(f"{first_position}{second_position}")
                                possible_moves = []
                                moves+=1
                
                # Click move
                if first_position in possible_moves:
                    print(prev_location, first_position)
                    piece_class.move(prev_location, first_position)
                    moves_lst.append(f"{prev_location}{first_position}")
                    possible_moves = []
                    moves+=1

                
                all_white_moves, all_black_moves = all_piece_moves()

                down = False # makes down variable false because dragged piece is no longer being dragged.


                # checks if king is in checkmate for white             
                if 'w_king' in list(board.values()):  
                    color = 'w'
                    king_piece = piece_classes.get('king')(f"{color}_king", get_key_by_value(board, f"{color}_king"), color)
                    checkmate = king_piece.in_checkmate(all_black_moves if result1[0]=='w' else all_white_moves)
                    if checkmate:
                        print("CHECKMATE for white")
                        pygame.quit()
                        sys.exit()
        
        # chessboard
        screen.blit(chessboard_img, (0,0))


        # show selected piece's moves
        show_moves(possible_moves, color_piece, moves, selected_piece_posX, selected_piece_posY)

        # draw existing pieces
        draw_pieces()

        if down:
            try:
                screen.blit(piece_locations.get(result1), (mouse_x-35, mouse_y-35))
            except:
                continue
        # checks if piece is in check, if so it will draw square around the king in check.
        draw_check(piece_classes, all_white_moves, all_black_moves, cause_piece=result1)

        # update the display
        pygame.display.flip()

        await asyncio.sleep(0)


asyncio.run(main())