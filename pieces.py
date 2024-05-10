from boards import board, piece_locations


class Piece:
    def __init__(self, name, pos, color):
        self.name = name
        self.pos = pos
        self.color = color

    def move(self, pos1, pos2):
        '''
        Swaps pos1 value to pos2. sets pos1 value to " ".
        '''
        pos1 = pos1
        pos2 = pos2
        board[pos1] = " "
        board[pos2] = self.name


def get_key_by_value(dicti, value):
    for key,val in dicti.items():
        if val == value:
            return key


class Pawn(Piece):
    def __init__(self, name, pos, color):
        super().__init__(name,pos, color)

    def possible_move_directions(self):
        col_letters = ['h','g','f','e','d','c','b','a', 'unused']
        # solid moves
        col, row = self.pos[0], int(self.pos[1])
        possible_moves = []
        start_pos = ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'] if self.color=='w' else ['a2','b2','c2','d2','e2','f2','g2','h2']
        number_of_moves = (3 if self.pos in start_pos else 2)
        for i in range(1, number_of_moves):
            move_position = f"{col}{row-i}" if self.color == 'w' else f"{col}{row+i}"
            try:
                if board[move_position] != " ":
                    break
                else:
                    possible_moves.append(move_position)
            except:
                continue

        # attack moves
        col, row = self.pos[0], int(self.pos[1])
        possible_move_attacks = []
        for idx, i in enumerate(col_letters):
            if col == i:
                attack_positions = [f"{col_letters[idx-1]}{row-1}", f"{col_letters[idx+1]}{row-1}"] if self.color == 'w' else [f"{col_letters[idx-1]}{row+1}", f"{col_letters[idx+1]}{row+1}"]
                for attack_position in attack_positions:
                    try:
                        if (board[attack_position].startswith('b_') and self.color == 'w') or (board[attack_position].startswith('w_') and self.color == 'b'):
                            possible_move_attacks.append(attack_position)
                    except:
                        continue
        return possible_moves + possible_move_attacks

class Knight(Piece):
    def __init__(self, name, pos, color):
        super().__init__(name,pos,color)

    def possible_move_directions(self):
        col_letters = ['unused','h','g','f','e','d','c','b','a', 'unused', 'unused1']
        
        # solid & attack moves
        col, row = self.pos[0], int(self.pos[1])
        possible_moves = []
        idxs = [1, 2] if self.color == 'w' else [(-1), (-2)]
        for idx, c in enumerate(col_letters):
            if c == col:
                move_or_attack_positions = [f"{col_letters[idx-idxs[0]]}{row-idxs[1]}", f"{col_letters[idx+idxs[0]]}{row-idxs[1]}", f"{col_letters[idx-idxs[0]]}{row+idxs[1]}", f"{col_letters[idx+idxs[0]]}{row+idxs[1]}",
                                            f"{col_letters[idx-idxs[1]]}{row-idxs[0]}", f"{col_letters[idx+idxs[1]]}{row+idxs[0]}", f"{col_letters[idx+idxs[1]]}{row-idxs[0]}", f"{col_letters[idx-idxs[1]]}{row+idxs[0]}"]
                for move_or_attack_pos in move_or_attack_positions:
                    if 'unused' not in move_or_attack_pos:
                        try:
                            if ((int(move_or_attack_pos[1:])) <= 8 and (int(move_or_attack_pos[1:])) >=0) and not board[move_or_attack_pos].startswith(self.color):
                                possible_moves.append(move_or_attack_pos)
                                possible_moves.append(move_or_attack_pos)
                        except:
                            continue
        return possible_moves


class Bishop(Piece):
    def __init__(self, name, pos, color):
        super().__init__(name, pos, color)
