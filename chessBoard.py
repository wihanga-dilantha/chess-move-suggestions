import chess

def generate_html_board(board):
    html_board = ""

    light_square_color = "#f0d9b5"
    dark_square_color = "#b58863"
    # Iterate through the ranks and files of the chess board
    for rank in range(8, 0, -1):
        html_board += "<div class='row'>"
        for file in range(1, 9):
            square_index = chess.square(file - 1, rank - 1)
            piece = board.piece_at(square_index)
            square_color = light_square_color if (rank + file) % 2 == 0 else dark_square_color
            html_board += f"<div class='square' style='background-color: {square_color};'>{get_piece_symbol(piece)}</div>"
        html_board += "</div>"

    return html_board

def get_piece_symbol(piece):
    if piece is None:
        return ""
    elif piece.color == chess.WHITE:
        if piece.piece_type == chess.PAWN:
            return "&#9817;"
        elif piece.piece_type == chess.ROOK:
            return "&#9814;"
        elif piece.piece_type == chess.KNIGHT:
            return "&#9816;"
        elif piece.piece_type == chess.BISHOP:
            return "&#9815;"
        elif piece.piece_type == chess.QUEEN:
            return "&#9813;"
        else:  # King
            return "&#9812;"
    else:  # Black pieces
        if piece.piece_type == chess.PAWN:
            return "&#9823;"
        elif piece.piece_type == chess.ROOK:
            return "&#9820;"
        elif piece.piece_type == chess.KNIGHT:
            return "&#9822;"
        elif piece.piece_type == chess.BISHOP:
            return "&#9821;"
        elif piece.piece_type == chess.QUEEN:
            return "&#9819;"
        else:  # King
            return "&#9818;"
