from boards import board
from pieces import King


def check_checkmate(positions, color):
    positions = list(set(positions))
    for position in positions:
        pass