import pandas as pd
import numpy as np
import scipy.stats as sps
import matplotlib.pyplot as plt

import chess
import chess.engine
import chessboard
from chessboard import display
import chess.svg

def its_draw(board):
    draw = False
    if (board.is_stalemate() or # draw
        board.is_fivefold_repetition() or 
        board.is_insufficient_material() or
        board.is_seventyfive_moves() or 
        board.can_claim_draw() #inclues 3 fold repetition and 50 move rule
        ):
        draw = True
    return draw

def simple_board_score(board):
    if board.is_checkmate():
        if board.turn:
            score = -np.inf #white was checkmated
        else:
            score = np.inf #black was checkmated
    elif its_draw(board):
        score = 0.0
    else:
        score = 0.0
        for (piece, value) in [(chess.PAWN, 100), 
                               (chess.BISHOP, 333), 
                               (chess.KING, 2000), 
                               (chess.QUEEN, 950), 
                               (chess.KNIGHT, 305),
                               (chess.ROOK, 563)]:
            score = (score + 
                     len(board.pieces(piece, chess.WHITE))*
                     value)
            score = (score - 
                     len(board.pieces(piece, chess.BLACK))*
                     value)
        #end for
    #end if
    return score



def minimax(board, depth, alpha, beta):
    if (depth==0) or (board.is_game_over()) or (its_draw(board)):
        return simple_board_score(board)
    else:
        if board.turn:
            best_score = -np.inf
            for move in board.legal_moves:
                board.push(move)
                score = minimax(board, depth-1, alpha, beta)
                best_score = np.max([score, best_score])
                alpha = np.max([alpha, best_score])
                board.pop()
                if beta <= alpha:
                    break
        else:
            best_score = np.inf
            for move in board.legal_moves:
                board.push(move)
                score = minimax(board, depth-1, alpha, beta)
                best_score = np.min([score, best_score])
                beta = np.min([beta, best_score])
                board.pop()
                if beta <= alpha:
                    break

    return best_score



def map_move_score(board, depth):
    legal_moves = board.legal_moves
    scores = []
    moves = []
    
    for move in legal_moves:
        board.push(move)
        score = minimax(board, depth, -np.inf, np.inf)
        scores.append(score)
        moves.append(move)
        board.pop()
    moves_scores_map = pd.DataFrame(
                          {'Score':scores,'Move':moves}
                        ).sort_values('Score')
    return moves_scores_map

def get_best_move(board, depth, is_white_turn):
    moves_scores_map = map_move_score(board, depth)

    if is_white_turn:
        best_move = moves_scores_map['Move'].values[-1]
        best_score = moves_scores_map['Score'].values[-1]
    else:
        best_move = moves_scores_map['Move'].values[0]
        best_score = moves_scores_map['Score'].values[0]
    print("best_move: " + best_move.uci())
    print("best_score: " + str(best_score))
    return best_move



board = chess.Board("r1b1kb1r/ppp2ppp/2n1pn2/1B1pq3/3PPQ2/2N5/PPP2PPP/R1B1K1NR w KQkq - 0 7")
score = simple_board_score(board)
print("score: " + str(score))
engine = chess.engine.SimpleEngine.popen_uci('./stockfish-ubuntu-x86-64-avx2')
# stockfish = engine.play(board,
#                 limit=chess.engine.Limit(2))
# stock_move = stockfish.move

# board.push(stock_move)
count = 1
# while (not board.is_game_over()) and (not its_draw(board)):
#     move_best = get_best_move(board,2,True)

#     board.push(move_best)

#     ## Stockfish plays
#     stockfish = engine.play(board,
#                    limit=chess.engine.Limit(1))
#     stock_move = stockfish.move

#     board.push(stock_move)
#     count += 1
#end while

print("end score: " + str(score))
print(board)
chess.svg.board(board, size=350)