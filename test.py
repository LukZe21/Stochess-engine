import ctypes
import os

lib = ctypes.CDLL(os.path.abspath("sample.dll"))

lib.getPosition.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]
lib.getPosition.restype = ctypes.c_char_p

pos_index = [["a8","a7","a6","a5","a4","a3","a2","a1"], ["b8","b7","b6","b5","b4","b3","b2","b1"], ["c8","c7","c6","c5","c4","c3","c2","c1"], ["d8","d7","d6","d5","d4","d3","d2","d1"],
             ["e8","e7","e6","e5","e4","e3","e2","e1"], ["f8","f7","f6","f5","f4","f3","f2","f1"], ["g8","g7","g6","g5","g4","g3","g2","g1"], ["h8","h7","h6","h5","h4","h3","h2","h1"]]

flat_pos_index = [item for sublist in pos_index for item in sublist]
char_arr = (ctypes.c_char_p*len(flat_pos_index))(*[ctypes.c_char_p(item.encode()) for item in flat_pos_index])

char_ptr_arr = ctypes.cast(char_arr, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))

result = lib.getPosition(500, 100, char_ptr_arr)


board = {"b_rook1": "a8","b_knight1": "b8", "b_bishop1": "c8","b_queen": "d8","b_king": "e8","b_bishop2": "f8","b_knight2": "g8","b_rook2": "h8",
         "b_pawn1": "a7","b_pawn2": "b7", "b_pawn3": "c7","b_pawn4": "d7", "b_pawn5": "e7","b_pawn6": "f7","b_pawn7": "g7","b_pawn8": "h7",
         " ": "a6"," ": "b6", " ": "c6"," ": "d6"," ": "e6"," ": "f6"," ": "g6"," ": "h6",
         " ": "a5"," ": "b5", " ": "c5"," ": "d5"," ": "e5"," ": "f5"," ": "g5"," ": "h5",
         " ": "a4"," ": "b4", " ": "c4"," ": "d4"," ": "e4"," ": "f4"," ": "g4"," ": "h4",
         " ": "a3"," ": "b3", " ": "c3"," ": "d3"," ": "e3"," ": "f3"," ": "g3"," ": "h3",
         "w_pawn1": "a2","w_pawn2": "b2", "w_pawn3": "c2","w_pawn3": "d2", "w_pawn3": "e2","w_pawn3": "f2","w_pawn3": "g2","w_pawn3": "h2",
         "w_rook1": "a1","w_knight1": "b1", "w_bishop1": "c1","w_queen": "d1","w_king": "e1","w_bishop2": "f1","w_knight2": "g1","w_rook2": "h1"}


lib.movePiece.argtypes = [ctypes.c_char_p, ctypes.py_object]
lib.movePiece.restype = ctypes.c_char_p

result = lib.movePiece(b'a2', board)
print(result)