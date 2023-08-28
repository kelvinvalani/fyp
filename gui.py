import tkinter as tk
from tkinter import messagebox
import chess
import csv
import time
class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess puzzles")
        
        self.chessboard = []
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        self.buttonEasy = tk.Button(self.main_frame, text="Easy", command=self.open_screenEasy)
        self.buttonMedium = tk.Button(self.main_frame, text="Medium", command=self.open_screenMedium)
        self.buttonHard = tk.Button(self.main_frame, text="Hard", command=self.open_screenHard)
        self.quit_button = tk.Button(self.main_frame, text="Quit", command=self.root.quit)

        self.buttonEasy.pack()
        self.buttonMedium.pack()
        self.buttonHard.pack()
        self.quit_button.pack()

        self.screens = [self.main_frame]
        self.current_screen = self.main_frame

    def open_screenEasy(self):
        self.show_new_screen("Easy puzzle")

    def open_screenMedium(self):
        self.show_new_screen("Medium puzzle")

    def open_screenHard(self):
        self.show_new_screen("Hard puzzle")

    def show_new_screen(self, screen_name):
        new_frame = tk.Frame(self.root)
        tk.Label(new_frame, text=screen_name).pack()
        
        back_button = tk.Button(new_frame, text="Back", command=lambda: self.go_back(new_frame))
        back_button.pack()

        move_button = tk.Button(new_frame, text="Make move", command=lambda: self.solve_puzzle())
        move_button.pack()

        self.current_screen.pack_forget()  # Hide the current screen
        new_frame.pack()  # Show the new screen
        self.screens.append(new_frame)
        self.current_screen = new_frame

        self.chessboard = [
    ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
    ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
    ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
]
        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.pack()
        self.draw_board()

    def draw_board(self):
        # Draw the chessboard
        for row in range(8):
            for col in range(8):
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50

                color = "white" if (row + col) % 2 == 0 else "grey"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        # Draw the pieces on the chessboard
        for row in range(8):
            for col in range(8):
                piece = self.chessboard[row][col]
                x = col * 50+25
                y = row * 50+25
                self.canvas.create_text(x, y, text=piece, font=("Arial", 24),fill="black")

    def make_move(self,move):
        self.update_chessboard(str(move))

    def update_chessboard(self, move):
        """
        Updates the chessboard based on the given move in algebraic notation.

        Args:
            chessboard (list): The current state of the chessboard as a 2D list.
            move (str): The move in algebraic notation, e.g., "e2e4".

        Returns:
            list: The updated chessboard after applying the move.
        """
        # Convert algebraic notation to row and column indices
        src_col, src_row = ord(move[0]) - ord('a'), 8 - int(move[1])
        dest_col, dest_row = ord(move[2]) - ord('a'), 8 - int(move[3])

        # Get the piece to be moved
        piece = self.chessboard[src_row][src_col]

        # Move the piece to the destination
        self.chessboard[src_row][src_col] = ' '  # Empty the source square
        self.chessboard[dest_row][dest_col] = piece  # Move the piece to the destination

        self.canvas.delete("all")
        self.canvas.pack_forget()

        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.pack()
        self.draw_board()

    def go_back(self, frame):
        if len(self.screens) > 1:
            self.screens.pop()
            self.current_screen.pack_forget()  # Hide the current screen
            self.canvas.delete("all")
            self.canvas.pack_forget()
            self.current_screen = self.screens[-1]
            self.current_screen.pack()  # Show the previous screen
        else:
            messagebox.showinfo("Info", "Cannot go back further.")

    def fen_to_2d_array(self,fen):
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
    
    def solve_puzzle(self):
        csv_file_path = "./lichess_puzzles.csv"

        # Read the CSV and play through puzzles
        with open(csv_file_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  # Skip the header row

            for row in csv_reader:
                dummy = input("Press enter for a new puzzle")
                puzzle_id, fen, moves, rating, *_ = row  # Unpack only the first 4 columns, ignore the rest

                print(f"Starting puzzle with ID: {puzzle_id}, Rating: {rating}")

                # Initialize a chess board with the FEN from the puzzle
                board = chess.Board(fen)

                self.chessboard = self.fen_to_2d_array(fen)
                self.draw_board()

                # Split the moves string into a list of individual moves
                moves_list = moves.split(" ")

                # Iterate through pairs of moves
                for i in range(0, len(moves_list), 2):
                    puzzle_move = moves_list[i]

                    # Apply the first puzzle move
                    dummy = input("Press enter to see opponents move")
                    if chess.Move.from_uci(puzzle_move) in board.legal_moves:
                        board.push(chess.Move.from_uci(puzzle_move))
                        # Display board
                        self.make_move(puzzle_move)
                    else:
                        print(f"Illegal puzzle move: {puzzle_move}. Skipping to next puzzle.")
                        break

                    if i+1 < len(moves_list):
                        player_move = moves_list[i+1]
                        print(player_move)
                        # Ask for the player's move
                        user_move = input('Your move (in UCI format, e.g., e2e4): ')

                        # Check if the move is the same as the puzzle's suggested move
                        if user_move != player_move:
                            print("Incorrect move. Try again.")
                            continue
                        
                        # Check if the move is legal
                        if chess.Move.from_uci(user_move) in board.legal_moves:
                            board.push(chess.Move.from_uci(user_move))
                            self.make_move(user_move)
                        else:
                            print("Illegal move. Try again.")
                            continue


if __name__ == "__main__":
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()
