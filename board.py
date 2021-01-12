from random import sample

class Board:

    def __init__(self):
        self.boardDim = 3
        self.boardSize = self.boardDim*self.boardDim

    # // operator indicates floor division
    def pattern(self, r,c): return (self.boardDim*(r%self.boardDim)+r//self.boardDim+c)%self.boardSize

    def shuffle(self, s): return sample(s,len(s)) 

    def generateBoard(self): 
        self.setUpBoard()
        board = [ [self.nums[self.pattern(r,c)] for c in self.cols] for r in self.rows ]
        squares = self.boardSize*self.boardSize
        empties = squares * 3//4
        for p in sample(range(squares),empties):
            board[p//self.boardSize][p%self.boardSize] = 0
        return board

    def setUpBoard(self):
        dimRange = range(self.boardDim) 
        self.rows  = [ g*self.boardDim + r for g in self.shuffle(dimRange) for r in self.shuffle(dimRange) ] 
        self.cols  = [ g*self.boardDim + c for g in self.shuffle(dimRange) for c in self.shuffle(dimRange) ]
        self.nums  = self.shuffle(range(1,self.boardDim*self.boardDim+1))
