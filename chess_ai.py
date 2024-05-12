import pygame
from boards import board
import re
import random


class ChessAI:
    def __init__(self, ):
        self.color = 'b'
    
    def generate_move(remaining_pieces):
        try:
            piece = random.choice(remaining_pieces)
            return piece
        except:
            None