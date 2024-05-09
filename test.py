import ctypes
import os

lib = ctypes.CDLL(os.path.abspath("sample.dll"))

lib.getMoves.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
lib.getMoves.restype = ctypes.c_char_p

white_pieces_location = [0, 100, 100, 200, 200, 300, 300, 400]
int_array = (ctypes.c_int * len(white_pieces_location))(*white_pieces_location)


result = lib.getMoves(300, 350, int_array, len(white_pieces_location))
print(result.decode())