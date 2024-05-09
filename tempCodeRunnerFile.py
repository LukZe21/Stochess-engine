import ctypes
import os

lib = ctypes.CDLL(os.path.abspath("sample.dll"))


class Pieces(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_char_p),
        ("location", ctypes.c_char_p)
    ]

lib.createPieces.restype = ctypes.POINTER(Pieces)

pieces_instance = lib.createPieces()

pieces_instance.contents.name = ctypes.c_char_p(b"Bishop")
pieces_instance.contents.location = ctypes.c_char_p(b"a6")

print(f"Name: {pieces_instance.contents.name.decode()}")
print(f"Location: { pieces_instance.contents.location.decode()}")

lib.destroyPieces.argtypes = [ctypes.POINTER(Pieces)]
lib.destroyPieces(pieces_instance)