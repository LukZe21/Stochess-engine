import random
import re
import time
from pieces import Pawn, Knight, Bishop, Rook, Queen, King
from boards import board

piece_classes = {'pawn': Pawn, 'knight': Knight, 'bishop': Bishop, 'rook': Rook, 'queen': Queen, 'king': King}
def get_key_by_value(dicti, value):
    for key,val in dicti.items():
        if val == value:
            return key


class ChessAI:
    def __init__(self):
        self.color = 'b'
        #'b_pawn': -10, 'b_knight':-30, 'b_bishop':-30, 'b_rook':-50, 'b_queen':-90, 'b_king':-900, 

    def generate_move(remaining_pieces):
        best_score, best_piece, pos = 0, None, None
        piece_scores = {'w_pawn':10, 'w_knight':30, 'w_bishop':30, 'w_rook':50, 'w_queen':90, 'w_king':900, ' ': 1}
        for piece in remaining_pieces:
            piece_for_dict = ''.join(filter(str.isalpha, piece))
            piece_class = piece_classes.get(piece_for_dict[1:])(piece, get_key_by_value(board, piece), 'b')
            possible_moves = piece_class.possible_move_directions()
            if possible_moves != []:
                for key, val in piece_scores.items():
                    for possible_move in possible_moves:
                        if re.search(key, rf"{board.get(possible_move)}") and val > best_score:
                            best_score = val
                            pos = possible_move
                            best_piece = piece

        # if there is no pieces to catch, go with a random move.
        if best_score <= 1:
            random_possible_move = None
            while not random_possible_move:
                try:
                    random_piece = random.choice(remaining_pieces)
                    piece_for_dict = ''.join(filter(str.isalpha, random_piece))
                    piece_class = piece_classes.get(piece_for_dict[1:])(random_piece, get_key_by_value(board, random_piece), 'b')
                    random_possible_move = random.choice(piece_class.possible_move_directions())
                except:
                    continue
            return random_possible_move, random_piece
        return pos, best_piece