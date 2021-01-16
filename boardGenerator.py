from random import sample
from board import Board

class BoardGenerator:

    def __init__(self, board):
        self.completedBoard = board
        self.boardSize = Board().getBoardSize()
        self.board = []
        self.initBoard()

    def initBoard(self):
        for i in range(9):
            list = []
            for j in range(9):
                list.append(0)
            self.board.append(list)
        return self.board

    def generateBoard(self):
        squares = self.boardSize * self.boardSize
        empties = squares * 1//4
        for p in sample(range(squares),empties):
            self.board[p//self.boardSize][p%self.boardSize] = self.completedBoard[p//self.boardSize][p%self.boardSize]
        return self.board