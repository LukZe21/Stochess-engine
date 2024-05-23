import pygame

pygame.mixer.init()
WIDTH, HEIGHT = 800, 800

bishop_black = pygame.image.load("imgs/Pieces/white_bishop.png")
knight_black = pygame.image.load("imgs/Pieces/white_knight.png")
queen_black = pygame.image.load("imgs/Pieces/white_queen.png")
king_black = pygame.image.load("imgs/Pieces/white_king.png")
rook_black = pygame.image.load("imgs/Pieces/white_rook.png")
pawn_black = pygame.image.load("imgs/Pieces/white_pawn.png")

bishop_white = pygame.image.load("imgs/Pieces/black_bishop.png")
knight_white = pygame.image.load("imgs/Pieces/black_knight.png")
queen_white = pygame.image.load("imgs/Pieces/black_queen.png")
king_white = pygame.image.load("imgs/Pieces/black_king.png")
rook_white = pygame.image.load("imgs/Pieces/black_rook.png")
pawn_white = pygame.image.load("imgs/Pieces/black_pawn.png")


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

piece_imgs = {'w_queen': queen_white, 'w_rook': rook_white, 'w_bishop': bishop_white, 'w_knight': knight_white,
              'b_queen': queen_black, 'b_rook': rook_black, 'b_bishop': bishop_black, 'b_knight': knight_black}


pos_index = [["a1","a2","a3","a4","a5","a6","a7","a8"], ["b1","b2","b3","b4","b5","b6","b7","b8"], ["c1","c2","c3","c4","c5","c6","c7","c8"], ["d1","d2","d3","d4","d5","d6","d7","d8"],
    ["e1","e2","e3","e4","e5","e6","e7","e8"], ["f1","f2","f3","f4","f5","f6","f7","f8"], ["g1","g2","g3","g4","g5","g6","g7","g8"], ["h1","h2","h3","h4","h5","h6","h7","h8"]]


col_convert_dict = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7} # converting letters into numbers (for columns)


# chessboard image
chessboard_img = pygame.image.load("imgs/Board/chessboard.png")
chessboard_img = pygame.transform.scale(chessboard_img, (WIDTH, HEIGHT))

# sounds
piece_move = pygame.mixer.Sound('sounds/piece_move.mp3')
piece_capture = pygame.mixer.Sound('sounds/piece_capture.mp3')
game_start = pygame.mixer.Sound('sounds/game-start.mp3')
game_end = pygame.mixer.Sound('sounds/game-end.mp3')
illegal_move = pygame.mixer.Sound('sounds/illegal.mp3')
move_check = pygame.mixer.Sound('sounds/move-check.mp3')
castle = pygame.mixer.Sound('sounds/castle.mp3')