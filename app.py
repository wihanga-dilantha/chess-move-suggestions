from flask import Flask, render_template, request, jsonify
import chess
from minmax import predict_best_move, predict_top_5_moves, print_board_position, model, predict_moves
from chessBoard import generate_html_board
from chess import Board

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    user_text = request.form['user_text']
    moves = user_text.split()

    board = chess.Board()
    illegal_moves = []
    moves_before_z = []
    moves_after_z = []
    empty_move_found = False

    for move_number, move in enumerate(moves, start=1):
        if 'z' in move.lower():
            empty_move_found = True
            break

        moves_before_z.append(move)

        try:
            board.push_san(move)
        except ValueError:
            illegal_moves.append({'move': move, 'move_number': move_number})
            break

    if empty_move_found:

        fen_before_z = chess.Board()
        for move in moves_before_z:
            fen_before_z.push_san(move)

        predictions = predict_moves(fen_before_z.fen())



        moves = ' '.join(moves_before_z)
        move_sequence = 'After:' + moves
        message='empty move found in sequence'

        fen = fen_before_z.fen()
        board = Board(fen)
        html_board = generate_html_board(board)
        
        return render_template('empty.html', message = message , move_sequence = move_sequence , html_board=html_board ,top_5_moves=predictions)
    
    elif illegal_moves:
        return jsonify({'message': 'Illegal move found', 'illegal_moves': illegal_moves})
    else:
        return jsonify({'message': 'All moves are legal'})

# @app.route('/predict_move', methods=['POST'])
# def predict_move():

#     fen_before_z = chess.Board()
#     for move in moves_before_z:
#             fen_before_z.push_san(move)
#     predictions = predict_moves(fen_before_z.fen())

#     return render_template('empty.html',top_5_moves=predictions)

if __name__ == '__main__':
    app.run(debug=True)
