#Eval and min max
import numpy
import chess
import chess.engine
import tensorflow
from tensorflow.keras.models import load_model

# Load the model from the specified file path
model = load_model(r'C:\Users\Wihanga Dilantha\Desktop\The App\myflaskenv\model.h5')

# Function to convert square index to matrix indices
def square_to_index(square):
    letter = chess.square_name(square)
    return 8 - int(letter[1]), ord(letter[0]) - ord('a')

# Function to encode the board for model input
def encode_board(board):
    squares_index = {
        'a': 0, 'b': 1, 'c': 2, 'd': 3,
        'e': 4, 'f': 5, 'g': 6, 'h': 7
    }


# split dims
def split_dims(board):
    board3d = numpy.zeros((14, 8, 8), dtype=numpy.int8)

    # Add pieces' view on the matrix
    for piece in chess.PIECE_TYPES:
        for square in board.pieces(piece, chess.WHITE):
            idx = numpy.unravel_index(square, (8, 8))
            board3d[piece - 1][7 - idx[0]][idx[1]] = 1
        for square in board.pieces(piece, chess.BLACK):
            idx = numpy.unravel_index(square, (8, 8))
            board3d[piece + 5][7 - idx[0]][idx[1]] = 1

        # Add attacks and valid moves
    aux = board.turn
    board.turn = chess.WHITE
    for move in board.legal_moves:
        i, j = square_to_index(move.to_square)
        board3d[12][i][j] = 1
    board.turn = chess.BLACK

    for move in board.legal_moves:
        i, j = square_to_index(move.to_square)
        board3d[13][i][j] = 1
    board.turn = aux

    return board3d

    encoded_board = split_dims(board)
    return encoded_board

# Function to convert moves string to FEN and matrix representation
def moves_to_matrix(moves_str):
    moves = moves_str.split()
    board = chess.Board()

    for move in moves:
        board.push(chess.Move.from_uci(move))

    fen = board.fen()
    matrix_rep = encode_board(board)

    return fen, matrix_rep

#minimax evaluation
def minimax_eval(board):
    board3d = split_dims(board)
    board3d = numpy.expand_dims(board3d, 0)
    return model.predict(board3d)[0][0]


def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return minimax_eval(board)

    if maximizing_player:
        max_eval = -numpy.inf
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = numpy.inf
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta,eval)
            if beta <= alpha:
                break
    return min_eval

def get_ai_move(board, depth):
    max_move = None
    max_eval = -numpy.inf

    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth -1, -numpy.inf,numpy.inf, False)
        board.pop()
        if eval > max_eval:
            max_eval = eval
            max_move = move

    return max_move

#make predictions

def predict_best_move(board, model):
    legal_moves = list(board.legal_moves)
    best_move = None
    best_move_score = -numpy.inf  # Initialize with negative infinity

    for move in legal_moves:
        board.push(move)
        score = minimax(board, 1, -numpy.inf , numpy.inf , False)  # Depth set to 1 for demonstration
        board.pop()

        # Update the best move if the current move has a higher score
        if score > best_move_score:
            best_move_score = score
            best_move = move

    return best_move

def predict_top_5_moves(board, model):
    legal_moves = list(board.legal_moves)

    # Create a list to store moves along with their scores
    moves_with_scores = []

    for move in legal_moves:
        board.push(move)
        score = minimax_eval(board)  # Use your model's evaluation function
        board.pop()

        # Append the move along with its score to the list
        moves_with_scores.append((move, score))

    # Sort the moves by their scores in descending order
    moves_with_scores.sort(key=lambda x: x[1], reverse=True)

    # Extract the top 5 moves from the sorted list
    top_5_moves = [move for move, _ in moves_with_scores[:5]]

    return top_5_moves

def print_board_position(board):
    print("Current Board Position:")
    print(board)
    print("FEN:", board.fen())


def predict_moves(position):

    #moves_sequence = position
    #uci_moves = standard_algebraic_to_uci(moves_sequence)#position convert into UCI

    #fen_position = moves_to_matrix(uci_moves)#make FEN

    custom_board_position = chess.Board(position)  # Custom FEN position

    print_board_position(custom_board_position)  # Print custom board position

    best_move = predict_best_move(custom_board_position.copy(), model)  # Predict best move for the custom position
    print("\nPredicted Best Move:", best_move)

    top_5_moves = predict_top_5_moves(custom_board_position.copy(), model)  # Predict top 5 moves for the custom position

    return (top_5_moves)

#function moves sequence convert to UCI 
def standard_algebraic_to_uci(moves_str):
    moves = moves_str.split()
    uci_moves = []

    board = chess.Board()
    for move in moves:
        move_obj = chess.Move.from_uci(board.parse_san(move).uci())
        uci_moves.append(move_obj.uci())
        board.push(move_obj)

    return ' '.join(uci_moves)

def moves_to_matrix(moves_str):
    moves = moves_str.split()
    board = chess.Board()

    for move in moves:
        board.push(chess.Move.from_uci(move))

    fen = board.fen()

    return fen
