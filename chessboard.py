
from detectionPCB import *


class Chessboard:
    def __init__(self):
        # self.columnAB = HallEffectBoard(0x40,0x41)
        self.columnCD = HallEffectBoard(0x42,0x43)
        # self.columnEF = HallEffectBoard(0x44,0x45)
        # self.columnGH = HallEffectBoard(0x46,0x47)
        # self.columnIJ = HallEffectBoard(0x48,0x49)
        # self.columnKL = HallEffectBoard(0x4A,0x4B)

    def read_board_state(self):

        # columnA,columnB = self.columnAB.read_board()
        columnC,columnD = self.columnCD.read_board()
        # columnE,columnF = self.columnEF.read_board()
        # columnG,columnH = self.columnGH.read_board()
        # columnI,columnJ = self.columnIJ.read_board()
        # columnK,columnL = self.columnKL.read_board()


        chessBoard = [columnC[::-1],columnD]

        return chessBoard

    def printLocations(self,board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    letter = chr(i+65)
                    pos = str(j+1)
                    print("A piece was detected on " , letter+pos)


if __name__ == "__main__":
    chessboard = Chessboard()
    try:
        while True:
            current_board = chessboard.read_board_state()
            chessboard.printLocations(current_board)
            time.sleep(2)

    except KeyboardInterrupt:
        pass