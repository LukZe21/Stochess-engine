import pygame
import asyncio
import sys
import re
from assets import board, piece_locations, pos_index, col_convert_dict, piece_move, piece_capture, game_start, game_end, illegal_move, move_check, chessboard_img, WIDTH, HEIGHT
from pieces import Pawn, Knight, Bishop, King, Queen, Rook
from stockfishBot import start_stockfish, set_skill_level, stockfish_move
from buttons import restart_button

fresh_board = board.copy()

piece_classes = {'pawn': Pawn, 'knight': Knight, 'bishop': Bishop, 'rook': Rook, 'queen': Queen, 'king': King}

def get_key_by_value(dicti, value):
    for key,val in dicti.items():
        if val == value:
            return key

moves = 1 # how many moves has been made (is being used to determine which side's turn it is)

# resizing chess pieces
for key, val in piece_locations.items():
    piece_locations[key] = pygame.transform.scale(val, (80,80))

def getPosition(mouseX, mouseY, pos_index):
    return pos_index[mouseX//100][mouseY//100]


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Chess")

# game icon
stochess_icon = pygame.image.load('imgs/Stochess_icon.png') 
pygame.display.set_icon(stochess_icon)



ROWS,COLUMNS = 8, 8

SQUARE_SIZE = HEIGHT / ROWS


def draw_pieces():
    ''' Draws and updates the board '''
    for pos, val in board.items():
        try:
            col = col_convert_dict[pos[0]]
            row = (int(pos[1]))-1
            if val != " ":
                screen.blit(piece_locations.get(val), ((col)*SQUARE_SIZE+SQUARE_SIZE//2-40, (row)*SQUARE_SIZE+SQUARE_SIZE//2-40))
        except:
            continue


def show_moves(directions, color, moves, mouseX, mouseY):
    ''' Shows possible moves for selected piece '''
    # this if statement is needed in order to encounter the bug with pieces merging into one another.
    if moves%2==0 and color=='w' or moves%2==1 and color=='b':
        position_of_piece = getPosition(mouseX, mouseY, pos_index)
        col = col_convert_dict[position_of_piece[0]]
        row = int(position_of_piece[1])-1
        pygame.draw.rect(screen, (209, 250, 47), ((col * SQUARE_SIZE), (row * SQUARE_SIZE) + 1, 100, 101))

        for pos in directions:
            col = col_convert_dict[pos[0]]
            row = int(pos[1])-1
            if board.get(pos).startswith('b_'):
                pygame.draw.circle(screen, (245, 66, 66), ((col * SQUARE_SIZE) + SQUARE_SIZE // 2, (row * SQUARE_SIZE) + SQUARE_SIZE // 2), 45, width=5)
            else:
                pygame.draw.circle(screen, (219, 219, 219), ((col * SQUARE_SIZE) + SQUARE_SIZE // 2, (row * SQUARE_SIZE) + SQUARE_SIZE // 2), 25)


def all_piece_moves(board_dict, all_white_moves=[], all_black_moves=[]):
    ''' returns the two list(for black and white pieces) of all possible moves pieces are available to make. '''

    for key, piece in board_dict.items():
        if piece != " ":
            if piece[2:] not in ['queen', 'king']:
                piece_class = piece_classes.get(piece[2:-1])(piece, key, piece[0])
                if 'pawn' in piece[2:]:
                    possible_moves = piece_class.possible_attack_moves(board_dict)
                else:
                    possible_moves = piece_class.possible_move_directions(board_dict)

                if piece[0] == 'w':
                    all_white_moves = all_white_moves+possible_moves
                else:
                    all_black_moves = all_black_moves+possible_moves

            elif piece[2:] in ['queen', 'king']:
                piece_class = piece_classes.get(piece[2:])(piece, key, piece[0])
                if piece[2:] == 'king' and piece[0]=='w':
                    possible_moves = piece_class.possible_move_directions(all_black_moves, board_dict)
                elif piece[2:] == 'king' and piece[0]=='b':
                    possible_moves = piece_class.possible_move_directions(all_white_moves, board_dict)
                else:
                    possible_moves = piece_class.possible_move_directions(board_dict)

                if piece[0] == 'w':
                    all_white_moves = all_white_moves + possible_moves
                else:
                    all_black_moves = all_black_moves + possible_moves
    return all_white_moves, all_black_moves


def possible_legal_moves(piece_that_caused_check, all_possible_moves_for_selected_piece, name_of_the_piece):
    cause_piece_rslt = ''.join(filter(str.isalpha, piece_that_caused_check))
    possible_block_moves = piece_classes.get(cause_piece_rslt[1:])(piece_that_caused_check, get_key_by_value(board, piece_that_caused_check), piece_that_caused_check[0]).possible_move_directions(board)
    possible_block_moves += get_key_by_value(board, piece_that_caused_check)
    legal_moves = []
    for move in all_possible_moves_for_selected_piece:
        if move in possible_block_moves:
            board2 = board.copy()
            board2[move] = name_of_the_piece
            king = define_piece('w_king', get_key_by_value(board2, 'w_king'), 'b')
            _, all_black_moves = all_piece_moves(board2)
            if not king.in_checkmate(all_black_moves, board2):
                legal_moves.append(move)
                break
    return legal_moves


def draw_check(piece_classes, all_white_moves, all_black_moves, cause_piece):
    """ Draws square around the king piece that is in check. """
    try:
        cause_piece_rslt = ''.join(filter(str.isalpha, cause_piece))
        possible_block_moves = piece_classes.get(cause_piece_rslt[1:])(cause_piece, get_key_by_value(board, cause_piece), cause_piece[0]).possible_move_directions(board)

        white_king = 'w_king'
        pos = get_key_by_value(board, white_king)
        col, row = pos[0], int(pos[1])-1
        king_piece = piece_classes.get('king')(white_king, pos, white_king[0])

        # CHECK for white
        check = king_piece.in_checkmate(all_black_moves)
        if check:
            for move in all_white_moves:
                if move in possible_block_moves:
                    pygame.draw.rect(screen, (128,0,0), ((col_convert_dict[col] * SQUARE_SIZE) + SQUARE_SIZE // 2 - 40, (row * SQUARE_SIZE) + SQUARE_SIZE // 2 - 40, 80, 80), 4)

        black_king = 'b_king'
        pos = get_key_by_value(board, black_king)
        col, row = pos[0], int(pos[1])-1
        king_piece = piece_classes.get('king')(black_king, get_key_by_value(board, black_king), black_king[0])

        # CHECK for black
        check = king_piece.in_checkmate(all_white_moves)
        if check:
            for move in all_black_moves:
                if move in possible_block_moves:
                    pygame.draw.rect(screen, (0,0,128), ((col_convert_dict[col] * SQUARE_SIZE) + SQUARE_SIZE // 2 - 40, (row * SQUARE_SIZE) + SQUARE_SIZE // 2 - 40, 80, 80), 4)
    except:
        None

    
def define_piece(piece, pos, color):
    piece_for_dict = ''.join([p for p in piece if p.isalpha()])
    piece_class = piece_classes.get(piece_for_dict[1:])(piece, pos, color)
    return piece_class


# starts and sets skill level for stockfish chess bot
start_stockfish()
set_skill_level(20)


# main game loop
async def main():
    game_start.play() # game start sound
    global board
    global moves
    possible_moves = []
    result1 = None
    color_piece = None
    selected_piece_posX, selected_piece_posY = None, None
    moves_lst = []
    down = False # determines what piece user has selected to drag
    king_in_check = False
    temp = None

    restart_game = False
    
    made_move = False  

    while True:
        # functionality of restart_button - if clicked game will restart to it's default
        if restart_game:
            print("- LET THE NEW GAME BEGIN -")
            board = fresh_board.copy()
            board2 = fresh_board.copy()
            made_move = False
            moves_lst = []
            all_white_moves, all_black_moves = all_piece_moves(board_dict=board)
            moves = 1
            restart_game = False
        
        # if it is white's turn stockfish will make a move.
        if moves%2==1:
            best_move = stockfish_move(moves_lst) # returns best move for white
            if best_move != "(none)":
                try:
                    temp = board.get(best_move[:2])
                    board[best_move[:2]] = " "

                    if board[best_move[2:]].startswith('w_'):
                        piece_capture.play() # capture sound

                    board[best_move[2:]] = temp
                    piece_class = define_piece(temp, best_move[2:], 'b')

                    if 'king' not in temp:
                        piece_possible_directions = piece_class.possible_move_directions(board)
                        
                    # if white king is in pieces possible directions
                    white_king = define_piece('w_king', get_key_by_value(board, 'w_king'), 'w')
                    white_king_pos = white_king.pos 

                    if white_king_pos in piece_possible_directions:
                        move_check.play() # check sound
                        king_in_check = True
                    else:
                        piece_move.play() # move sound
                        king_in_check = False
                    board2 = board.copy()

                except:
                    continue

            else:
                board = fresh_board.copy()
                board2 = fresh_board.copy()
                moves_lst = []
                all_white_moves, all_black_moves = all_piece_moves(board_dict=board)
            moves+=1
        
        for event in pygame.event.get():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            all_white_moves, all_black_moves = all_piece_moves(board)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                board2 = board.copy() # for dragging the piece (for it to get removed from place it was selected.)
                # restart button
                if restart_button.is_over(event.pos):
                    restart_game = True

                # for click move
                prev_location = get_key_by_value(board, result1)

                # Drag and Drop move
                first_position = getPosition(mouse_x, mouse_y, pos_index) # what is board idx of square user has clicked on
                result1 = board.get(first_position) # what piece(or nothing) is on first_position variable

                if result1 != " ":
                    print(f"{first_position} : {result1}")

                if result1.startswith('w_'):
                    selected_piece_posX, selected_piece_posY = mouse_x, mouse_y
                    for piece in ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']:
                        if re.search(rf"{piece}", result1):
                            if re.search(rf"king", result1):
                                piece_class = piece_classes.get(piece)(result1, first_position, result1[0])
                                possible_moves = piece_class.possible_move_directions(all_black_moves, board)
                            else:
                                piece_class = piece_classes.get(piece)(result1, first_position, result1[0])
                                possible_moves = piece_class.possible_move_directions(board)
                                if king_in_check:
                                    possible_moves = possible_legal_moves(temp, possible_moves, result1)
                            color_piece = result1[0] # what color is a piece
                down = True # makes down variable true for dragging selected piece.

            elif event.type == pygame.MOUSEBUTTONUP:
                black_king = define_piece('b_king', get_key_by_value(board, 'b_king'), 'b')
                black_king_pos = black_king.pos 

                # Drag and Drop move
                second_position = getPosition(mouse_x, mouse_y, pos_index) # pretty much does the same thing as above variables do.
                result2 = board.get(second_position)

                if result1.startswith('w_') and moves%2==0:
                    if result1 != " " and (result1[0]+result2[0] != 'ww') and (result1[0]+result2[0]!='bb'): #result1 and result2 should not be same color pieces
                            if second_position in possible_moves:
                                if board.get(second_position).startswith('b'):
                                    piece_capture.play()
                                piece_class.move(first_position, second_position, board)
                                # board2 = board.copy()
                                made_move = True
                                    
                                moves_lst.append(f"{first_position}{second_position}")

                                all_white_moves, all_black_moves = all_piece_moves(board)

                                if black_king_pos in all_white_moves:
                                    move_check.play() # check sound
                                else:
                                    piece_move.play()
                                    
                                possible_moves = []
                                moves+=1
                            else:
                                illegal_move.play()
                
                # Click move
                if first_position in possible_moves:
                    if board.get(second_position).startswith('b'):
                        piece_capture.play()
                    piece_class.move(prev_location, first_position, board)
                    made_move = True
                    moves_lst.append(f"{prev_location}{first_position}")
                    possible_moves = []
                    moves+=1

                    if black_king_pos in all_white_moves:
                        move_check.play() # check sound
                    else:
                        piece_move.play()
                        possible_moves = []
                    
                all_white_moves, all_black_moves = all_piece_moves(board)

                # checks if king is in checkmate for white  
                if moves%2==1: # (if it is black's turn)
                    if 'w_king' in list(board.values()):  
                        color = 'w'
                        king_piece = piece_classes.get('king')(f"{color}_king", get_key_by_value(board, f"{color}_king"), color)
                        checkmate = king_piece.in_checkmate(all_black_moves if result1[0]=='w' else all_white_moves)
                        if checkmate:
                            board = fresh_board.copy()
                            board2 = fresh_board.copy()
                            moves_lst = []
                            all_white_moves, all_black_moves = all_piece_moves(board_dict=board)

                down = False # makes down variable false because dragged piece is no longer being dragged.

                # if move has not been made board will go back to how it was.
                if not made_move:
                    board = board2.copy()
                made_move = False
            
        # chessboard
        screen.blit(chessboard_img, (0,0))

        # show selected piece's moves
        show_moves(possible_moves, color_piece, moves, selected_piece_posX, selected_piece_posY)

        # draw existing pieces
        draw_pieces()

        # for dragging pieces
        if down and result1 != " ":
            board[get_key_by_value(board, result1)] = " "
            screen.blit(piece_locations.get(result1), (mouse_x-35, mouse_y-35))
    

        # checks if piece is in check, if so it will draw square around the king in check.
        draw_check(piece_classes, all_white_moves, all_black_moves, cause_piece=result1)

        restart_button.draw(screen)

        # update the display
        pygame.display.flip()
        
        await asyncio.sleep(0)

asyncio.run(main())