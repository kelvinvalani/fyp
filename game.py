import tkinter as tk
from tkinter import messagebox
import chess
import csv
import time
import random
from chessboard import *
from driver import *

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess puzzles")
        self.whiteGrave = 0
        self.blackGrave = 0

        self.white_pawns = 3
        self.white_rook = 1
        self.white_knight = 1
        self.white_king = 1

        self.black_pawns = 2
        self.black_rook = 1
        self.black_knight = 1
        self.black_king = 1
        self.black_bishop = 1

        self.chessboard = []
        self.driver = Driver("A1")
        self.physical_board = Chessboard()
        self.prev_board_state = self.physical_board.read_board_state()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()
        # Define new frames here
        self.chessboard_frame = tk.Frame(self.main_frame, bg="white")
        self.chessboard_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.control_frame = tk.Frame(self.main_frame, bg="lightgray")
        self.control_frame.pack(pady=10, padx=20, fill=tk.X)

        self.message_frame = tk.Frame(self.main_frame, bg="white")
        self.message_frame.pack(pady=10, padx=20, fill=tk.X)

        self.buttonEasy = tk.Button(
            self.control_frame, 
            text="Easy", 
            command=self.open_screenEasy, 
            font=("Helvetica", 14, "bold"), 
            bg="#86C232", 
            fg="white",
            width=15, 
            height=2, 
            borderwidth=2, 
            relief="solid"
        )
        self.buttonMedium = tk.Button(
            self.control_frame, 
            text="Medium", 
            command=self.open_screenMedium, 
            font=("Helvetica", 14, "bold"), 
            bg="#FFA500", 
            fg="white",
            width=15, 
            height=2, 
            borderwidth=2, 
            relief="solid"
        )
        self.buttonHard = tk.Button(
            self.control_frame, 
            text="Hard", 
            command=self.open_screenHard, 
            font=("Helvetica", 14, "bold"), 
            bg="#FF4500", 
            fg="white",
            width=15, 
            height=2, 
            borderwidth=2, 
            relief="solid"
        )
        self.quit_button = tk.Button(
            self.control_frame, 
            text="Quit", 
            command=self.root.quit, 
            font=("Helvetica", 14, "bold"), 
            bg="#DC143C", 
            fg="white",
            width=15, 
            height=2, 
            borderwidth=2, 
            relief="solid"
        )

        self.buttonEasy.pack()
        self.buttonMedium.pack()
        self.buttonHard.pack()
        self.quit_button.pack()

        self.screens = [self.main_frame]
        self.current_screen = self.main_frame

    def open_screenEasy(self):
        csv_file_path = "./1.easy_puzzles.csv"
        self.show_new_screen("Easy puzzle", csv_file_path)

    def open_screenMedium(self):
        csv_file_path = "./2.med_puzzles.csv"
        self.show_new_screen("Medium puzzle", csv_file_path)

    def open_screenHard(self):
        csv_file_path = "./3.hard_puzzles.csv"
        self.show_new_screen("Hard puzzle", csv_file_path)
    
    def go_back_to_main(self):
        # Hide the current screen
        self.current_screen.pack_forget()
        # Show the main menu screen
        self.main_frame.pack()
        self.current_screen = self.main_frame  # Update the current screen
        

    def show_new_screen(self, screen_name, csv_file_path):
        self.current_screen.pack_forget()  # Hide the current screen
        main_container = tk.Frame(root)
        main_container.pack(padx=15, pady=15, expand=True, fill='both')
        self.current_screen = main_container

        # Adding a label to display the screen name
        title_label = tk.Label(main_container, text=screen_name, font=("Arial", 24, "bold"), bg="white")
        title_label.pack(pady=10)

        chessboard_frame = tk.Frame(main_container)
        chessboard_frame.pack(side='top', padx=10, pady=10)

        # Adding a canvas for the chessboard
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
        self.canvas = tk.Canvas(chessboard_frame, width=414, height=414)
        self.canvas.pack()
        self.draw_board()

        control_frame = tk.Frame(main_container, bg="lightgray")
        control_frame.pack(side='top', fill='both', expand=True, padx=5, pady=5)

        start_button = tk.Button(control_frame, text="Start",command=lambda: self.solve_puzzle(csv_file_path))
        hint_button = tk.Button(control_frame, text="Hint", command=lambda: self.hint())
        nextpuzzle_button = tk.Button(control_frame, text="Next puzzle", command=lambda: self.nextpuzzle())
        back_button = tk.Button(control_frame, text="Back", command=self.go_back_to_main)


        hint_button.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        nextpuzzle_button.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        start_button.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
        back_button.grid(row=0, column=3, padx=5, pady=5, sticky='nsew')


        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)
        control_frame.grid_columnconfigure(2, weight=1)
        control_frame.grid_columnconfigure(3, weight=1)
        control_frame.grid_columnconfigure(4, weight=1)
        control_frame.grid_columnconfigure(5, weight=1)

        # Message Frame
        message_frame = tk.Frame(main_container, bg="white", padx=10, pady=5)
        message_frame.pack(side='bottom', fill='both', expand=True, padx=5, pady=5)
        self.message_label = tk.Label(message_frame, text=' ', bg="white", font=("Arial", 16), wraplength=750, justify="left")
        self.message_label.pack(fill='both', expand=True)     

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

        # Draw the row numbers (1 to 8)
        for row in range(8):
            y = row * 50 + 25
            self.canvas.create_text(408, y, text=str(8 - row), font=("Arial", 10), fill="black")

        # Draw the column letters (a to h)
        for col in range(8):
            x = col * 50 + 25
            self.canvas.create_text(x, 408, text=chr(col + ord('a')), font=("Arial", 10), fill="black")

    def detectPlayerMove(self):
        previousState = self.prev_board_state
        currentState = self.physical_board.read_board_state()
        # logic to detect movement
        source = ''
        destination = ''

        for i in range(len(previousState)):
            for j in range(len(previousState[i])):
                if previousState[i][j] != currentState [i][j]:
                    if previousState[i][j] == 0:
                        source = chr(i+63) + str(j+1)
                    else:
                        destination = chr(i+63) + str(j+1)

        move = source + destination
        print("original move: " + move)
        if len(move) == 4:
            if move[0] in '?@ij' or move[2] in '?@ij':
                move = 'captured'
                self.prev_board_state = self.physical_board.read_board_state()
        elif len(move) <4:
            move = 'captured'
        return move.lower()
    
    def make_robot_move(self,move):
        start_square = move.upper()[:2]
        end_square = move.upper()[2:]

        start_square = chr(ord(start_square[0])+2)+start_square[1]
        end_square = chr(ord(end_square[0])+2)+end_square[1]
        
        dest_col, dest_row = ord(move[2]) - ord('a'), 8 - int(move[3])
        if self.chessboard[dest_row][dest_col] != '':
            if self.chessboard[dest_row][dest_col] in  ['♜', '♞', '♝', '♛', '♚','♟']:
                if self.blackGrave < 8:
                    grave_square = "K" + str(self.blackGrave + 1)
                else:
                    grave_square = "L" + str(self.blackGrave - 8 + 1)
                
                self.blackGrave = self.blackGrave + 1
            else:
                if self.whiteGrave < 8:
                    grave_square = "A" + str(self.whiteGrave + 1)
                else:
                    grave_square = "B" + str(self.whiteGrave - 8 + 1)
                
                self.whiteGrave = self.whiteGrave + 1
                
                            
            self.driver.move_piece(end_square,grave_square)



        self.driver.move_piece(start_square, end_square)

    def make_move(self,move):
        self.update_chessboard(str(move))   

    def record_move(self):
        self.prev_board_state = self.physical_board.read_board_state()

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

        #self.canvas.delete("all")
        #self.canvas.pack_forget()

        #self.canvas = tk.Canvas(root, width=800, height=800)
        #self.canvas.pack()
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
                    new_row.extend([''] * int(char))
                else:
                    new_row.append(pieces_mapping.get(char, char))
            board.append(new_row)

        return board
    
    def setup_board(self):
        for i in range(len(self.chessboard)):
            for j in range(len(self.chessboard)):
                if self.chessboard[i][j] == '♙':
                    sourceColumn = 'A'
                    sourceRow = self.white_pawns+1
                    source = sourceColumn + str(sourceRow)
                    destinationColumn = chr(67+j)
                    destinationRow = 8-i
                    destinaton = destinationColumn + str(destinationRow)
                    self.white_pawns = self.white_pawns -1
                    self.driver.move_piece(source,destinaton)
                elif self.chessboard[i][j] == '♘':
                    sourceColumn = 'A'
                    sourceRow = self.white_knight+4
                    source = sourceColumn + str(sourceRow)
                    destinationColumn = chr(67+j)
                    destinationRow = 8-i
                    destinaton = destinationColumn + str(destinationRow)
                    self.white_knight = self.white_knight -1
                    self.driver.move_piece(source,destinaton)
                elif self.chessboard[i][j] == '♔':
                    sourceColumn = 'A'
                    sourceRow = self.white_king+7
                    source = sourceColumn + str(sourceRow)
                    destinationColumn = chr(67+j)
                    destinationRow = 8-i
                    destinaton = destinationColumn + str(destinationRow)
                    self.white_king = self.white_king -1
                    self.driver.move_piece(source,destinaton)
                elif self.chessboard[i][j] == '♖':
                    sourceColumn = 'A'
                    sourceRow = self.white_rook+6
                    source = sourceColumn + str(sourceRow)
                    destinationColumn = chr(67+j)
                    destinationRow = 8-i
                    destinaton = destinationColumn + str(destinationRow)
                    self.white_rook = self.white_rook -1
                    self.driver.move_piece(source,destinaton)
                elif self.chessboard[i][j] == '♜':
                    sourceColumn = 'K'
                    sourceRow = self.black_rook+6
                    source = sourceColumn + str(sourceRow)
                    destinationColumn = chr(67+j)
                    destinationRow = 8-i
                    destinaton = destinationColumn + str(destinationRow)
                    self.black_rook = self.black_rook -1
                    self.driver.move_piece(source,destinaton)
                elif self.chessboard[i][j] == '♝':
                    sourceColumn = 'K'
                    sourceRow = self.black_bishop+5
                    source = sourceColumn + str(sourceRow)
                    destinationColumn = chr(67+j)
                    destinationRow = 8-i
                    destinaton = destinationColumn + str(destinationRow)
                    self.black_bishop = self.black_bishop -1
                    self.driver.move_piece(source,destinaton)
                elif self.chessboard[i][j] == '♞':
                    sourceColumn = 'K'
                    sourceRow = self.black_knight+4
                    source = sourceColumn + str(sourceRow)
                    destinationColumn = chr(67+j)
                    destinationRow = 8-i
                    destinaton = destinationColumn + str(destinationRow)
                    self.black_knight = self.black_knight -1
                    self.driver.move_piece(source,destinaton)
                elif self.chessboard[i][j] == '♚':
                    sourceColumn = 'K'
                    sourceRow = self.black_king+7
                    source = sourceColumn + str(sourceRow)
                    destinationColumn = chr(67+j)
                    destinationRow = 8-i
                    destinaton = destinationColumn + str(destinationRow)
                    self.black_king = self.black_king -1
                    self.driver.move_piece(source,destinaton)
                elif self.chessboard[i][j] == '♟':
                    sourceColumn = 'K'
                    sourceRow = self.black_pawns+2
                    source = sourceColumn + str(sourceRow)
                    destinationColumn = chr(67+j)
                    destinationRow = 8-i
                    destinaton = destinationColumn + str(destinationRow)
                    self.black_pawns = self.black_pawns -1
                    self.driver.move_piece(source,destinaton)
                else:
                    pass

                



    def solve_puzzle(self, csv_file_path):
        # Read the CSV and play through puzzles
        with open(csv_file_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  # Skip the header row

            all_rows = [row for row in csv_reader]  # Store all rows in a list
            # random.shuffle(all_rows)  # Shuffle the rows
            global board
            for row in all_rows:
                self.driver.relocalise()
                dummy = input("Press enter for a new puzzle")
                puzzle_id, fen, moves, rating, *_ = row  # Unpack only the first 4 columns, ignore the rest

                print(f"Starting puzzle with ID: {puzzle_id}, Rating: {rating}")

                # Initialize a chess board with the FEN from the puzzle
                board = chess.Board(fen)

                self.chessboard = self.fen_to_2d_array(fen)
                self.draw_board()
                #self.setup_board()
                # Split the moves string into a list of individual moves
                moves_list = moves.split(" ")

                # Iterate through pairs of moves
                for i in range(0, len(moves_list), 2):
                    puzzle_move = moves_list[i]
                    user_move = 0
                    global player_move
                    player_move = 1

                    # Apply the first puzzle move
                    dummy = input("Press enter to see opponents move")

                    if chess.Move.from_uci(puzzle_move) in board.legal_moves:
                        board.push(chess.Move.from_uci(puzzle_move))
                        # Display board
                        self.make_robot_move(puzzle_move)
                        self.update_chessboard(str(puzzle_move))
                    else:
                        print("Illegal move. Try again.")
                        continue

                    user_move = ''
                    while user_move != player_move:
                        player_move = moves_list[i+1]

                        #if nextpuzzle is pressed
                        #    break
                        # Ask for the player's move

                        while len(user_move) != 4 or user_move == 'captured' or user_move == "Incorrect move":
                            self.prev_board_state = self.physical_board.read_board_state()
                            dummy = input("Press enter to confirm a move/capture")
                            user_move = self.detectPlayerMove()
                            print(user_move)

                        if chess.Move.from_uci(user_move) in board.legal_moves:
                            board.push(chess.Move.from_uci(user_move))
                            self.make_move(user_move)
                            if user_move != player_move:
                                print("Incorrect move. Try again.")
                                continue
                            else:
                                print("Correct move!\n")
                                self.prev_board_state =self.physical_board.read_board_state()
                                continue
                        else:
                            user_move = "Incorrect move"
            
                print("Puzzle completed!\n")

    def hint(self):
        start_square = player_move[:2]
        start_square_index = chess.SQUARE_NAMES.index(start_square.lower())
        piece = board.piece_at(start_square_index)
        pieces_mapping = {
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
        }
        self.message_label.config(text=f"Move the {pieces_mapping.get(piece.symbol(), piece.symbol())} at {start_square}")

    def nextpuzzle(self):
        print("Skipping to next puzzle.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()
