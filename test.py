import ctypes
import os
import platform


lib = ctypes.CDLL("./sample.dll", **dict(winmode=1))


lib.getPosition.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]
lib.getPosition.restype = ctypes.c_char_p

pos_index = [["a8","a7","a6","a5","a4","a3","a2","a1"], ["b8","b7","b6","b5","b4","b3","b2","b1"], ["c8","c7","c6","c5","c4","c3","c2","c1"], ["d8","d7","d6","d5","d4","d3","d2","d1"],
             ["e8","e7","e6","e5","e4","e3","e2","e1"], ["f8","f7","f6","f5","f4","f3","f2","f1"], ["g8","g7","g6","g5","g4","g3","g2","g1"], ["h8","h7","h6","h5","h4","h3","h2","h1"]]

flat_pos_index = [item for sublist in pos_index for item in sublist]
char_arr = (ctypes.c_char_p*len(flat_pos_index))(*[ctypes.c_char_p(item.encode()) for item in flat_pos_index])

char_ptr_arr = ctypes.cast(char_arr, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))

result = lib.getPosition(500, 100, char_ptr_arr)
print(result.decode())