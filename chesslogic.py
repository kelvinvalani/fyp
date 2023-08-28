import csv
import chess

# Function to display the board in the terminal. Alternatively, you could use chess.svg.board() for graphical display
def display_board(board):
    print(board)

def fen_to_board_array(fen):
    # Split the FEN string to only take the piece positions
    piece_positions = fen.split(' ')[0]
    
    # Initialize an 8x8 board as a list of lists
    board_array = [['' for _ in range(8)] for _ in range(8)]
    
    row = 0
    col = 0
    
    for char in piece_positions:
        if char == '/':  # Move to the next row
            row += 1
            col = 0
        elif char.isnumeric():  # Empty squares
            col += int(char)
        else:  # There's a piece on this square
            board_array[row][col] = char
            col += 1

    return board_array

# Define the path to your CSV file
csv_file_path = "./lichess_puzzles.csv"

# Read the CSV and play through puzzles
with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)  # Skip the header row

    for row in csv_reader:
        puzzle_id, fen, moves, rating, *_ = row  # Unpack only the first 4 columns, ignore the rest

        print(f"Starting puzzle with ID: {puzzle_id}, Rating: {rating}")

        # Initialize a chess board with the FEN from the puzzle
        board = chess.Board(fen)

        # Display the board
        display_board(board)
        print(fen_to_board_array(fen))
        
        print(f"---------------")

        # Split the moves string into a list of individual moves
        moves_list = moves.split(" ")

        # Iterate through pairs of moves
        for i in range(0, len(moves_list), 2):
            puzzle_move = moves_list[i]

            # Apply the first puzzle move
            if chess.Move.from_uci(puzzle_move) in board.legal_moves:
                board.push(chess.Move.from_uci(puzzle_move))
            else:
                print(f"Illegal puzzle move: {puzzle_move}. Skipping to next puzzle.")
                break

            # Display board
            display_board(board)

            if i+1 < len(moves_list):
                player_move = moves_list[i+1]
                
                # Ask for the player's move
                user_move = input('Your move (in UCI format, e.g., e2e4): ')

                # Check if the move is the same as the puzzle's suggested move
                if user_move != player_move:
                    print("Incorrect move. Try again.")
                    continue
                
                # Check if the move is legal
                if chess.Move.from_uci(user_move) in board.legal_moves:
                    board.push(chess.Move.from_uci(user_move))
                else:
                    print("Illegal move. Try again.")
                    continue

                # Display board
                display_board(board)
                print(f"---------------")