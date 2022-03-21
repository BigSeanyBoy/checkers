from copy import deepcopy

class Board:
    
    def __init__(self, board_array=None, pieces=None, last_move=None, whose_turn=0):
        if board_array is None or pieces is None:
            self.generate_board()
        else:
            self.board_array = board_array
            self.pieces = pieces
            self.last_move = last_move
        self.whose_turn = whose_turn
            
    def generate_board(self):
        self.board_array = []
        self.pieces = [[], []]
        for x in range(100):
            if (x < 11 
                or x > 88 
                or x % 10 == 0 
                or x % 10 == 9
            ):
                self.board_array.append(99)
            elif (x in range(10, 19, 2) 
                  or x in range(21, 28, 2) 
                  or x in range(30, 39, 2)
            ):
                self.board_array.append(1)
                self.pieces[0].append([x, 1])
            elif (x in range(61, 68, 2) 
                  or x in range(70, 79, 2) 
                  or x in range(81, 88, 2)
            ):
                self.board_array.append(-1)
                self.pieces[1].append([x, -1])
            else:
                self.board_array.append(0)
                
    def get_pieces(self):
        return self.pieces
    
    def get_turn(self):
        return self.whose_turn
    
    def get_last_move(self):
        return self.last_move
                
    def get_possible_moves(self):
        possible_moves = []
        for piece in self.pieces[self.whose_turn]:
            if abs(piece[1]) == 2:
                jumps = [-11, -9, 9, 11]
            else:
                jumps = [9, 11]
            jump_from = piece[0]
            direction = int(piece[1] / abs(piece[1]))
            for jump in jumps:
                jump_to = jump_from + (jump * direction)
                if self.board_array[jump_to] == 99:
                    continue
                if self.board_array[jump_to] == 0:
                    possible_moves.append([jump_from, jump_to, False])
                elif abs(piece[1] - self.board_array[jump_to]) > 1:
                    jump_to = jump_from + (jump * direction * 2)
                    try:
                        if self.board_array[jump_to] == 0:
                            possible_moves.append([jump_from, jump_to, True])
                    except IndexError:
                        print(jump_from, jump_to)
        if any([move[2] for move in possible_moves]):
            possible_moves = [move for move in possible_moves if move[2]]
        return possible_moves
    
    def move_piece(self, move):
        self.last_move = move
        jump_from, jump_to, capture = move
        value = self.pieces[self.whose_turn][0][1]
        unit_value = value / abs(value)
        for piece in self.pieces[self.whose_turn]:
            if piece[0] == jump_from:
                piece[0] = jump_to
                if self.king_check(piece):
                    if abs(piece[1]) != 2:
                        piece[1] *= 2
                    unit_value *= 2
        self.board_array[jump_from] = 0
        self.board_array[jump_to] = unit_value
        if capture:
            opponent_pieces = self.pieces[abs(self.whose_turn - 1)]
            for i in range(len(opponent_pieces)):
                capture_pos = int((jump_from + jump_to) / 2)
                if opponent_pieces[i][0] == capture_pos:
                    opponent_pieces.pop(i)
                    self.board_array[capture_pos] = 0 
                    break
            if any([move[2] for move in self.get_possible_moves()]):
                self.switch_player()
                    
    def switch_player(self):
        self.whose_turn = abs(self.whose_turn - 1)
        
    def king_check(self, piece):
        if ((piece[1] == 1 
             and piece[0] > 80)
            or (piece[1] == -1
                and piece[0] < 20)
            or abs(piece[1] == 2)
           ):
            return True
        return False
    
    def king_distance(self, piece, enemy_pieces):
        avg_dist = 0
        for e_piece in enemy_pieces:
            row_dist = abs(int(piece[0] / 10) - int(e_piece[0] / 10))
            col_dist = abs((piece[0] % 10) - (e_piece[0] % 10))
            distance = ((row_dist ** 2) + (col_dist ** 2)) ** 0.5
            avg_dist += distance
        return avg_dist / len(enemy_pieces)
                    
    def is_game_over(self):
        if (not self.pieces[0] 
            or not self.pieces[1] 
            or not self.get_possible_moves()
        ):
            return True
        return False
    
    def copy(self):
        return deepcopy(self)
                
    def __str__(self):
        ret = ''
        for row in range(len(self.board_array), 0, -10):
            if row > 0 and row < 90:
                ret += '{}| '.format(int(row / 10))
                ret += ''.join([{1: 'b ', 2: 'B ', -1: 'w ', -2: 'W '}.get(x, '_ ') for x in self.board_array[row+1:row+9]])
                ret += '\n'
        ret += '  ----------------\n'
        ret += '   1 2 3 4 5 6 7 8'
        return ret