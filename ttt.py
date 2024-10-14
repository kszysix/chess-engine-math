import numpy as np
import sys
# to measure exec time 
from timeit import default_timer as timer 
print(sys.argv)
# tic tac toe

ttt_board_1 = [['-','-','-'],
               ['-','-','-'],
               ['-','-','-']]


ttt_board_2 = [['A','B','B'],
               ['A','A','-'],
               ['-','-','B']]

ttt_board_3 = [['-','-','B'],
               ['-','A','-'],
               ['-','-','-']]

print(ttt_board_1[1][1])

def its_draw(ttt_board):
    for i in range(3):
        for j in range(3):
            if ttt_board[i][j] == '-':
                return False
    return True

def its_won(ttt_board, user):
    if ttt_board[0][0] == user and ttt_board[1][1] == user and ttt_board[2][2] == user:
        return True
    if ttt_board[0][2] == user and ttt_board[1][1] == user and ttt_board[2][0] == user:
        return True
    
    for i in range(3):
        if ttt_board[0][i] == user and ttt_board[1][i] == user and ttt_board[2][i] == user:
            return True
        if ttt_board[i][0] == user and ttt_board[i][1] == user and ttt_board[i][2] == user:
            return True
        
    return False

def can_make_move(i,j,ttt_board):
    if ttt_board[i][j] == '-':
        return True
    return False

def make_move(i,j, ttt_board, user):
    ttt_board[i][j] = user
    return ttt_board

def undo_move(i,j, ttt_board):
    ttt_board[i][j] = '-'
    return ttt_board

user_a = 'A'
user_b = 'B'
def minimax_ttt(ttt_board, is_move_A, alpha, beta, use_alphabeta = False):
    minimax_value = -2 if is_move_A else 2
    user = user_a if is_move_A else user_b
    if its_won(ttt_board, user):
        return 1 if is_move_A else -1
    if its_draw(ttt_board):
        return 0

    for i in range(3):
        for j in range(3):
            if can_make_move(i,j, ttt_board):
                ttt_board_after = make_move(i,j,ttt_board,user)
                move_value = minimax_ttt(ttt_board_after, not is_move_A, alpha, beta, use_alphabeta)
                ttt_board = undo_move(i,j,ttt_board)
                if is_move_A:
                    if move_value > minimax_value:
                        minimax_value = move_value
                    alpha = max([alpha, minimax_value])  
                    if beta <= alpha and use_alphabeta:
                        # print("break move A, beta <= alpha, alpha : " + str(alpha) + " beta : " + str(beta))
                        break
                elif not is_move_A:
                    if move_value < minimax_value:    
                        minimax_value = move_value 
                    beta = min([beta, minimax_value])  
                    if beta <= alpha and use_alphabeta:
                        # print("break move B, beta <= alpha, alpha : " + str(alpha) + " beta : " + str(beta))
                        break

    return minimax_value

def print_board(ttt_board):
    print("----------------")
    print(ttt_board[0])
    print(ttt_board[1])
    print(ttt_board[2])
    print("_________________")

def get_best_move(ttt_board, is_move_A):
    best_i = 0
    best_j = 0
    best_score = -2 if is_move_A else 2
    user = user_a if is_move_A else user_b
    for i in range(3):
        for j in range(3):
            if can_make_move(i,j, ttt_board):
                ttt_board_after = make_move(i,j,ttt_board,user)
                if its_won(ttt_board_after, user):
                    best_score = 2 if is_move_A else -2
                    print("won move " + str(best_i) + " " + str(best_j) + " : " + str(best_score))
                    return i,j
                
                score = minimax_ttt(ttt_board_after, not is_move_A, -np.inf, np.inf, True)
                ttt_board = undo_move(i,j,ttt_board)
                if is_move_A and  score > best_score:
                    best_score = score
                    best_i = i
                    best_j = j
                elif not is_move_A  and  score < best_score:          
                    best_score = score 
                    best_i = i
                    best_j = j
                print("move " + str(i) + " " + str(j) + " : " + str(score))

    print("best move " + str(best_i) + " " + str(best_j) + " : " + str(best_score))
    return best_i, best_j



def make_game_move(ttt_board, is_move_A):
    best_i, best_j = get_best_move(ttt_board, is_move_A)
    user = user_a if is_move_A else user_b
    ttt_board = make_move(best_i, best_j, ttt_board, user)
    return ttt_board

def run_game(start_board):
    is_move_A = True
    print_board(start_board)
    while not (its_won(start_board, user_a) or its_won(start_board, user_b) or its_draw(start_board)):
        start_board = make_game_move(start_board, is_move_A)
        print_board(start_board)
        is_move_A = not is_move_A
    print_board(start_board)



def make_human_move(ttt_board, user):
    human_i = int(input("Get i: "))
    human_j = int(input("Get j: "))
    return make_move(human_i, human_j, ttt_board, user)


def run_game_with_human(start_board, is_human_A):
    if is_human_A:
        human_move = True
        human_user = user_a
    else:
        human_move = False
        human_user = user_b

    while not (its_won(start_board, user_a) or its_won(start_board, user_b) or its_draw(start_board)):
        
        if human_move:
            start_board = make_human_move(start_board, human_user)
        else:
            start_board = make_game_move(start_board, not is_human_A)
        human_move = not human_move
        print_board(start_board)

# is_human_int = 1 if len(sys.argv) < 2 else int(sys.argv[1])
# is_human_A = True if is_human_int == 1 else False
# run_game_with_human(ttt_board_1, is_human_A)

start = timer()
run_game(ttt_board_1)
print("ttt:", timer()-start)   