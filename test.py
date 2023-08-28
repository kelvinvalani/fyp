def fen_to_2d_array(fen):
    pieces_mapping = {
        'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
        'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
    }

    rows = fen.split('/')
    board = []

    for row in rows:
        new_row = []
        for char in row:
            if char.isdigit():
                new_row.extend(['.'] * int(char))
            else:
                new_row.append(pieces_mapping.get(char, char))
        board.append(new_row)

    return board

fen = "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR"
chess_board = fen_to_2d_array(fen)

print(chess_board)