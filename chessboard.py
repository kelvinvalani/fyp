
from detectionPCB import *


class Chessboard:
    def __init__(self):
        self.white_res = HallEffectBoard(0x0)
        self.columnAB = HallEffectBoard(0x10)
        self.columnCD = HallEffectBoard(0x20)
        self.columnEF = HallEffectBoard(0x30)
        self.columnGH = HallEffectBoard(0x40)
        #self.black_res = HallEffectBoard(0x50)

    def read_board_state(self):
        white_res_left,white_res_right = self.white_res.read_board()
        columnA,columnB = self.columnAB.read_board()
        columnC,columnD = self.columnCD.read_board()
        columnE,columnF = self.columnEF.read_board()
        columnG,columnH = self.columnGH.read_board()
        #black_res_left,black_res_right = self.black_res()

        chessBoard = [white_res_left,white_res_right,columnA,columnB,columnC,columnD,columnE,columnF,columnG,columnH]

        return chessBoard

    def printLocations(self,board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    print("Piece detecetd on square " , (i,j))


if __name__ == "__main__":
    chessboard = Chessboard()
    try:
        while True:
            current_board = chessboard.read_board_state()
            chessboard.printLocations(current_board)

    except KeyboardInterrupt:
        pass