import pygame


bishop_black = pygame.image.load("imgs/Pieces/black_bishop.png")
knight_black = pygame.image.load("imgs/Pieces/black_knight.png")
queen_black = pygame.image.load("imgs/Pieces/black_queen.png")
king_black = pygame.image.load("imgs/Pieces/black_king.png")
rook_black = pygame.image.load("imgs/Pieces/black_rook.png")
pawn_black = pygame.image.load("imgs/Pieces/black_pawn.png")

bishop_white = pygame.image.load("imgs/Pieces/white_bishop.png")
knight_white = pygame.image.load("imgs/Pieces/white_knight.png")
queen_white = pygame.image.load("imgs/Pieces/white_queen.png")
king_white = pygame.image.load("imgs/Pieces/white_king.png")
rook_white = pygame.image.load("imgs/Pieces/white_rook.png")
pawn_white = pygame.image.load("imgs/Pieces/white_pawn.png")


board = {"a8": "w_rook1", "b8": "w_knight1", "c8": "w_bishop1", "d8": "w_queen", "e8": "w_king", "f8": "w_bishop2", "g8": "w_knight2", "h8": "w_rook2",
         "a7": "w_pawn1", "b7": "w_pawn2", "c7": "w_pawn3", "d7": "w_pawn4", "e7": "w_pawn5", "f7": "w_pawn6", "g7": "w_pawn7", "h7": "w_pawn8",
         "a6": " ", "b6": " ", "c6": " ", "d6": " ", "e6": " ", "f6": " ", "g6": " ", "h6": " ",
         "a5": " ", "b5": " ", "c5": " ", "d5": " ", "e5": " ", "f5": " ", "g5": " ", "h5": " ",
         "a4": " ", "b4": " ", "c4": " ", "d4": " ", "e4": " ", "f4": " ", "g4": " ", "h4": " ",
         "a3": " ", "b3": " ", "c3": " ", "d3": " ", "e3": " ", "f3": " ", "g3": " ", "h3": " ",
         "a2": "b_pawn1", "b2": "b_pawn2", "c2": "b_pawn3", "d2": "b_pawn4", "e2": "b_pawn5", "f2": "b_pawn6", "g2": "b_pawn7", "h2": "b_pawn8",
         "a1": "b_rook1", "b1": "b_knight1", "c1": "b_bishop1", "d1": "b_queen", "e1": "b_king", "f1": "b_bishop2", "g1": "b_knight2", "h1": "b_rook2"}


piece_locations = {"w_rook1": rook_white,"w_knight1": knight_white,"w_bishop1": bishop_white,"w_queen": queen_white,
                    "w_king": king_white,"w_bishop2": bishop_white,"w_knight2": knight_white,"w_rook2": rook_white,
                    "w_pawn1": pawn_white, "w_pawn2":pawn_white, "w_pawn3":pawn_white, "w_pawn4":pawn_white, "w_pawn5":pawn_white,
                    "w_pawn6":pawn_white,"w_pawn7": pawn_white,"w_pawn8": pawn_white,           
                    "b_rook1": rook_black,"b_knight1":knight_black, "b_bishop1": bishop_black, "b_queen":queen_black,
                    "b_king": king_black,"b_bishop2": bishop_black, "b_knight2": knight_black, "b_rook2": rook_black,
                   "b_pawn1":pawn_black, "b_pawn2":pawn_black, "b_pawn3":pawn_black, "b_pawn4":pawn_black, "b_pawn5":pawn_black,
                   "b_pawn6":pawn_black, "b_pawn7":pawn_black, "b_pawn8":pawn_black}