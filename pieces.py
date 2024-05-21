from assets import board

def get_key_by_value(dicti, value):
    for key,val in dicti.items():
        if val == value:
            return key

class Piece:
    def __init__(self, name, pos, color):
        self.name = name
        self.pos = pos
        self.color = color

    def move(self, pos1, pos2, board_dict):
        ''' Swaps pos1 value to pos2. sets pos1 value to " ". '''
        board_dict[pos1] = " "
        board_dict[pos2] = self.name

    def get_rows_and_columns(self):
        return self.pos[0], int(self.pos[1])


class Pawn(Piece):
    def __init__(self, name, pos, color):
        super().__init__(name,pos, color)

    col_letters = ['h','g','f','e','d','c','b','a', 'unused']

    def possible_move_directions(self, board):  
        # solid moves
        col, row = self.get_rows_and_columns()
        # possible moves piece can take in given position.
        possible_moves = []
        #start position of pawn
        start_pos = ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'] if self.color=='w' else ['a2','b2','c2','d2','e2','f2','g2','h2']
        # number of moves will be different if pawn is at start position
        number_of_moves = (3 if self.pos in start_pos else 2)
        for i in range(1, number_of_moves):
            move_position = f"{col}{row-i}" if self.color == 'w' else f"{col}{row+i}"
            try:
                if board[move_position] != " ": # if move_position is not free the pawn will not be able to move.
                    break
                else:
                    possible_moves.append(move_position)
            except:
                continue
        
        possible_move_attacks = self.possible_attack_moves(board)
        
        # merging normal moves and attack moves into one list
        return possible_moves + possible_move_attacks 
    
    def possible_attack_moves(self, board):
        # attack moves
        col, row = self.pos[0], int(self.pos[1])
        possible_move_attacks = []
        for idx, i in enumerate(self.col_letters):
            if col == i:
                # possible attack positions
                attack_positions = [f"{self.col_letters[idx-1]}{row-1}", f"{self.col_letters[idx+1]}{row-1}"] if self.color == 'w' else [f"{self.col_letters[idx-1]}{row+1}", f"{self.col_letters[idx+1]}{row+1}"] 
                for attack_position in attack_positions:
                    try:
                        if (board[attack_position].startswith('b_') and self.color == 'w') or (self.color == 'b'):
                            possible_move_attacks.append(attack_position)
                    except:
                        continue
        return possible_move_attacks
            
            

class Knight(Piece):
    def __init__(self, name, pos, color):
        super().__init__(name,pos,color)

    def possible_move_directions(self, board):
        # Define the columns in reverse order to match the board's orientation
        col_letters = ['unused', 'h','g','f','e','d','c','b','a', 'unused', 'unused1']
        
        # solid & attack moves
        col, row = self.get_rows_and_columns()
        possible_moves = []
        idxs = [1, 2] if self.color == 'w' else [(-1), (-2)]
        for idx, c in enumerate(col_letters):
            if c == col:
                move_or_attack_positions = [f"{col_letters[idx-idxs[0]]}{row-idxs[1]}", f"{col_letters[idx+idxs[0]]}{row-idxs[1]}", f"{col_letters[idx-idxs[0]]}{row+idxs[1]}", f"{col_letters[idx+idxs[0]]}{row+idxs[1]}",
                                            f"{col_letters[idx-idxs[1]]}{row-idxs[0]}", f"{col_letters[idx+idxs[1]]}{row+idxs[0]}", f"{col_letters[idx+idxs[1]]}{row-idxs[0]}", f"{col_letters[idx-idxs[1]]}{row+idxs[0]}"]
                for move_or_attack_pos in move_or_attack_positions:
                    if 'unused' not in move_or_attack_pos:
                        try:
                            # row of an move_or_attack_pos has to be less ore equal to 8 and more or equal to 0
                            if ((int(move_or_attack_pos[1:])) <= 8 and (int(move_or_attack_pos[1:])) >=0) and not board[move_or_attack_pos].startswith(self.color):
                                possible_moves.append(move_or_attack_pos)
                                possible_moves.append(move_or_attack_pos)
                        except:
                            continue
        return possible_moves


class Bishop(Piece):
    def __init__(self, name, pos, color):
        super().__init__(name, pos, color)

    def possible_move_directions(self, board):
        col_letters = ['unused', 'unused1', 'unused2', 'unused3', 'unused4', 'h','g','f','e','d','c','b','a', 'unused', 'unused1', 'unused2', 'unused3', 'unused4']

        col, row = self.get_rows_and_columns()
        possible_moves = []
        opp_color = 'b' if self.color=='w' else 'w'
        for idx, c in enumerate(col_letters):
            if c==col:
                # generate the list of positions for each direction
                dir1 = [[idx - i, row - i] for i in range(8)]
                dir2 = [[idx + i, row + i] for i in range(8)]
                dir3 = [[idx + i, row - i] for i in range(8)]
                dir4 = [[idx - i, row + i] for i in range(8)]

                # combine the directions into a single list
                lst_of_positions = [dir1, dir2, dir3, dir4]

                for direction in lst_of_positions:
                    pos_possible_moves = []
                    for pos in direction:
                        try:
                            move_or_attack_position = f"{col_letters[pos[0]]}{pos[1]}"
                            # print([board[pos] for pos in possible_moves])
                            if (board[move_or_attack_position] != self.name and board[move_or_attack_position].startswith(self.color)) or (board[move_or_attack_position] != self.name and (opp_color in [board[pos][0] for pos in pos_possible_moves])):
                                break
                            if ('unused' not in col_letters[pos[0]]) and (8 >= pos[1] > 0) and (not board[move_or_attack_position].startswith(self.color)):
                                pos_possible_moves.append(move_or_attack_position)
                        except:
                            continue
                    possible_moves = possible_moves + pos_possible_moves
        return possible_moves


class Rook(Piece):
    def __init__(self, name, pos, color):
        super().__init__(name, pos, color)
    
    def possible_move_directions(self, board):
        col_letters = ['unused', 'unused', 'unused', 'unused', 'unused', 'unused', 'h','g','f','e','d','c','b','a', 'unused']

        col, row = self.get_rows_and_columns()
        possible_moves = []
        opp_color = 'b' if self.color=='w' else 'w'
        for idx, c in enumerate(col_letters):
            if c==col:
                # generate the list of positions for each direction
                dir1 = [[idx+i, row] for i in range(8)]
                dir2 = [[idx-i, row] for i in range(8)]
                dir3 = [[idx, row-i] for i in range(8)]
                dir4 = [[idx, row+(i)] for i in range(8)]

                # combine the directions into a single list
                move_or_attack_positions = [dir1,dir2,dir3,dir4]

                for direction in move_or_attack_positions:
                    pos_possible_moves = []
                    for pos in direction:
                        try:
                            move_or_attack_position = f"{col_letters[pos[0]]}{pos[1]}"
                            if (board[move_or_attack_position] != self.name and board[move_or_attack_position].startswith(self.color)) or (board[move_or_attack_position] != self.name and opp_color in [board[pos][0] for pos in pos_possible_moves]):
                                break
                            if ('unused' not in move_or_attack_position) and (8>=pos[1]>0) and (not board[move_or_attack_position].startswith(self.color)):
                                pos_possible_moves.append(move_or_attack_position)
                        except Exception as e:
                            continue
                    possible_moves = possible_moves + pos_possible_moves
        return possible_moves
    

class Queen(Piece):
    def __init__(self, name, pos, color):
        super().__init__(name, pos, color)

    def possible_move_directions(self, board):
        col_letters = ['unused', 'unused', 'unused', 'unused', 'h','g','f','e','d','c','b','a', 'unused', 'unused', 'unused', 'unused', 'unused', 'unused']

        col, row = self.get_rows_and_columns()
        opp_color = 'b' if self.color=='w' else 'w'
        possible_moves = []
        for idx, c in enumerate(col_letters):
            if c==col:
                # diagonal moves
                dir1 = [[idx - i, row - i] for i in range(8)]
                dir2 = [[idx + i, row + i] for i in range(8)]
                dir3 = [[idx + i, row - i] for i in range(8)]
                dir4 = [[idx - i, row + i] for i in range(8)]
                # straight moves
                dir5 = [[idx+i, row] for i in range(8)]
                dir6 = [[idx-i, row] for i in range(8)]
                dir7 = [[idx, row-i] for i in range(8)]
                dir8 = [[idx, row+(i)] for i in range(8)]
                move_or_attack_positions = [dir1,dir2,dir3,dir4,dir5,dir6,dir7,dir8]
                for direction in move_or_attack_positions:
                    pos_possible_moves = []
                    for pos in direction:
                        try:
                            move_or_attack_position = f"{col_letters[pos[0]]}{pos[1]}"
                            if (board[move_or_attack_position] != self.name and board[move_or_attack_position].startswith(self.color)) or (board[move_or_attack_position] != self.name and opp_color in [board[pos][0] for pos in pos_possible_moves]):
                                break
                            if ('unused' not in move_or_attack_position) and (8>=pos[1]>0) and (not board[move_or_attack_position].startswith(self.color)):
                                pos_possible_moves.append(move_or_attack_position)
                        except Exception as e:
                            continue
                    possible_moves = possible_moves + pos_possible_moves
        return possible_moves
    
class King(Piece):
    def __init__(self, name, pos, color):
        super().__init__(name,pos,color)

    def possible_move_directions(self, all_opponent_moves, board):
        col_letters = ['unused', 'h','g','f','e','d','c','b','a', 'unused']
        col, row = self.get_rows_and_columns()
        possible_moves = []
        move_pos_num = 1 if self.color=='w' else -1
        for idx, c in enumerate(col_letters):
            if c==col:
                move_or_attack_positions = [f"{col_letters[idx]}{row-(move_pos_num)}", f"{col_letters[idx-(move_pos_num)]}{row+(move_pos_num)}", f"{col_letters[idx+(move_pos_num)]}{row+(move_pos_num)}", f"{col_letters[idx-(move_pos_num)]}{row}", f"{col_letters[idx-(move_pos_num)]}{row-(move_pos_num)}", f"{col_letters[idx+(move_pos_num)]}{row}", f"{col_letters[idx+(move_pos_num)]}{row-(move_pos_num)}", f"{col_letters[idx]}{row+(move_pos_num)}"]
                for move_or_attack_position in move_or_attack_positions:
                    try:
                        if ('unused' not in move_or_attack_position) and (not board[move_or_attack_position].startswith(self.color)) and move_or_attack_position not in all_opponent_moves:
                            possible_moves.append(move_or_attack_position)
                    except:
                        continue
        return possible_moves
    
    def in_checkmate(self, all_opposite_moves, board=board):
        ''' Checks for check '''
        king_moves = self.possible_move_directions(all_opposite_moves, board)
        king_moves.append(self.pos)

        if self.pos in all_opposite_moves:
            return True
        return False