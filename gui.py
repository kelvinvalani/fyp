import tkinter as tk
from tkinter import messagebox

class SimpleGUI:
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

        move_button = tk.Button(new_frame, text="Make move", command=lambda: self.make_move())
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

    def make_move(self):
        print("Please make a move")
        move = input()
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

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()
