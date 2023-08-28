import tkinter as tk
# import Image, ImageTk
# Define the chessboard and pieces (using Unicode symbols)
# (Same as before)
chessboard = [
    ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
    ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
    ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
]
class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess GUI")
        self.just_launched = True
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
        self.main_menu()

    def main_menu(self):
        # Display the main menu with options
        if self.just_launched == False:
            self.back_button.pack_forget()
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.canvas.create_text(200, 100, text="Chess puzzles", font=("Arial", 20))

        self.start_button_easy = tk.Button(self.root, text="Easy", command=self.new_game)
        self.start_button_easy.pack(pady=10)

        self.start_button_medium = tk.Button(self.root, text="Medium", command=self.new_game)
        self.start_button_medium.pack(pady=10)

        self.start_button_hard = tk.Button(self.root, text="Hard", command=self.new_game)
        self.start_button_hard.pack(pady=10)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_game)
        self.quit_button.pack(pady=10)

    def new_game(self):
        # Clear the main menu and start a new game by drawing the chessboard
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
        self.canvas.delete("all")
        self.canvas.pack_forget()
        self.start_button_easy.pack_forget()
        self.start_button_medium.pack_forget()
        self.start_button_hard.pack_forget()
        self.quit_button.pack_forget()

        # Draw the chessboard
        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.pack()
        self.draw_board()


        # Show the back button
        self.back_button = tk.Button(root, text="Back to Main Menu", command=self.back_to_main_menu)
        self.back_button.pack()
        self.back_button.place(x=10, y=10)


        self.move_button = tk.Button(self.root, text="Make move", command=self.make_move)
        self.move_button.pack()
        self.move_button.place(x=100, y=200)

    def quit_game(self):
        self.root.destroy()

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


    def back_to_main_menu(self):
        # Clear the chessboard and go back to the main menu
        self.canvas.delete("all")
        self.canvas.pack_forget()
        self.back_button.pack_forget()  # Hide the back button
        self.move_button.pack_forget()

        # Display the main menu again
        self.just_launched =False
        self.main_menu()

    def make_move(self):
        print("Please make a move")
        move = input()
        self.update_chessboard(str(move))

if __name__ == "__main__":
    root = tk.Tk()
    chess_gui = ChessGUI(root)
    root.mainloop()
