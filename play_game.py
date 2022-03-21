from checkers_api import *
from ai import *
from boards import *
import time

avg_mmwoab = []
avg_mmwab = []

QUIT = ['q', 'Q', 'quit', 'Quit', 'QUIT']
YES = ['y', 'yes', 'Y', 'Yes', 'YES']
NO = ['n', 'no', 'N', 'No', 'NO']

def start_game(board=None):
    if board is None:
        board = Board()
    cont = True
    players_move = not board.get_turn()
    depth_limit = 9
    print('Starting board state:\n{}'.format(board))
    while cont:
        # Print the board state, then have someone take a turn
        if players_move:
            board, cont = player_turn(board)
            print()
            print('Score: {}'.format(heuristic_score(board)))
            print('Board state after player turn:\n{}\n'.format(board))
        else:
            board = ai_turn(board)
            print()
            print('Score: {}'.format(heuristic_score(board)))
            print('Board state after AI turn:\n{}\n'.format(board))

        # If the player wants to exit
        if cont is False:
            print_end(cont, player_name)

        # Switch whose turn it is
        board.switch_player()
        players_move = not board.whose_turn
        
        # If the game is over, print who wins and decide if a new game should be started
        if board.is_game_over():
            #cont = print_endgame(board, players_move)
            #board = Board()
            #print_end(cont, player_name)
            print('\n\nGame Over')
            break
        
def get_player_move():
    print("Which piece would you like to move?")
    player_response = [None, None]
    while player_response[0] is None:
        inp = input(">>> ")

        # Allow the player to quit gracefully
        if inp in QUIT:
            return player_response
        try:
            player_response[0] = int(inp)
        except:
            pass
        
    print("Where would you like to move your piece?")
    while player_response[1] is None:
        inp = input(">>> ")

        try:
            player_response[1] = int(inp)
        except:
            pass
    return player_response

def player_turn(board):
    player_move = get_player_move()
    cont = player_move[0] is not None
    if cont:
        possible_moves = board.get_possible_moves()
        try:
            move = [move for move in possible_moves if move[0:2] == player_move][0]
        except IndexError:
            return player_turn(board)
        board.move_piece(move)
    return board, cont

def ai_turn(board):
    #start = time.time()
    #move = minimax_ordered_alphabeta(board, 1)
    #end = time.time()
    #mmwoab = end-start
    #print('Minimax with Ordered AlphaBeta: {} seconds'.format(mmwoab))
    #start = time.time()
    #move = minimax_alphabeta(board, 1)
    #end = time.time()
    #print('Minimax with AlphaBeta: {} seconds'.format(end-start))
    start = time.time()
    move = progressive_deepening(board)
    end = time.time()
    print('Progressive Deepening: searched {} moves ahead in {} seconds'.format(move[3], end-start))
    board.move_piece(move[0][1].get_last_move())
    return board
        
if __name__ == '__main__':
    start_game()