from checkers_api import *
from boards import *
import time

DEPTH_LIM = 9

INF = float('inf')

def dummy_move(board):
    print(get_possible_states(board))
    return board.get_possible_moves()[0]

def heuristic_score(board):
    pieces = board.get_pieces()
    if len(pieces[0]) == 0:
        return 15
    elif len(pieces[1]) == 0:
        return -15
    maximizer_score = 0
    for piece in pieces[1]:
        if abs(piece[1]) == 1:
            maximizer_score += 1
        else:
            maximizer_score += 1.5
    #        maximizer_score += (5 + (9 - int(piece[0] / 10)))
    #    else:
    #        maximizer_score += 15
    minimizer_score = 0
    for piece in pieces[0]:
        if abs(piece[1]) == 1:
            minimizer_score += 1
        else:
            minimizer_score += 1.5
    #    if abs(piece[1]) == 1:
    #        minimizer_score += (5 + int(piece[0] / 10))
    #    else:
    #        minimizer_score += 15
    #return maximizer_score - minimizer_score
    return maximizer_score / minimizer_score

def next_states(board):
    states = []
    if board.is_game_over():
        return states
    for move in board.get_possible_moves():
        state = board.copy()
        state.move_piece(move)
        state.switch_player()
        states.append(state)
    return states

def minimax(board, maximizer, depth=0): 
    static_evals = 0
    if depth == DEPTH_LIM or board.is_game_over():
        return [[board], heuristic_score(board), 1]
    best_score = -INF if maximizer else INF
    best_path = None
    for move in board.get_possible_moves():
        clone = board.copy()
        clone.move_piece(move)
        clone.switch_player()
        path = minimax(clone, clone.get_turn(), depth+1)
        if maximizer:
            if path[1] > best_score:
                best_score = path[1]
                best_path = [board] + path[0]
        else:
            if path[1] < best_score:
                best_score = path[1]
                best_path = [board] + path[0]
        static_evals += path[2]
    return [best_path, best_score, static_evals]

def minimax_alphabeta(board, maximizer, depth=0, alpha=-INF, beta=INF):
    static_evals = 0
    if depth == DEPTH_LIM or board.is_game_over():
        return [[board], heuristic_score(board), 1]
    best_score = -INF if maximizer else INF
    best_path = None
    for move in board.get_possible_moves():
        clone = board.copy()
        clone.move_piece(move)
        clone.switch_player()
        path = minimax_alphabeta(clone, clone.get_turn(), depth+1, alpha, beta)
        if maximizer:
            if path[1] > best_score:
                best_score = path[1]
                best_path = [board] + path[0]
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        else:
            if path[1] < best_score:
                best_score = path[1]
                best_path = [board] + path[0]
            beta = min(beta, best_score)
            if alpha >= beta:
                break
        static_evals += path[2]
    return [best_path, alpha if maximizer else beta, static_evals]

def minimax_ordered_alphabeta(board, maximizer, depth=0, alpha=-INF, beta=INF, depth_lim=9):
    static_evals = 0
    if depth == depth_lim or board.is_game_over():
        return [[board], heuristic_score(board), 1]
    best_score = -INF if maximizer else INF
    best_path = None
    states = []
    for move in board.get_possible_moves():
        clone = board.copy()
        clone.move_piece(move)
        clone.switch_player()
        states.append(clone)
    if maximizer:
        states.sort(reverse=True, key=heuristic_score)
    else:
        states.sort(reverse=False, key=heuristic_score)
    for state in states:
        path = minimax_ordered_alphabeta(state, state.get_turn(), depth+1, alpha, beta, depth_lim)
        if maximizer:
            if path[1] > best_score:
                best_score = path[1]
                best_path = [board] + path[0]
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        else:
            if path[1] < best_score:
                best_score = path[1]
                best_path = [board] + path[0]
            beta = min(beta, best_score)
            if alpha >= beta:
                break
        static_evals += path[2]
    return [best_path, alpha if maximizer else beta, static_evals]

def progressive_deepening(state, depth_lim=INF, maximize=True):
    start = time.time()
    limit = 0
    while(time.time() - start < 30):
        limit += 1
        move = minimax_ordered_alphabeta(state, 1, depth_lim=limit)
        if limit == 1 and move[0][1].get_last_move()[2]:
            move.append(limit)
            return move
    move.append(limit)
    return move
    
    
    