from random import sample

boardDim = 3
boardSize = boardDim*boardDim

# // operator indicates floor division
def pattern(r,c): return (boardDim*(r%boardDim)+r//boardDim+c)%boardSize

def shuffle(s): return sample(s,len(s)) 
dimRange = range(boardDim) 
rows  = [ g*boardDim + r for g in shuffle(dimRange) for r in shuffle(dimRange) ] 
cols  = [ g*boardDim + c for g in shuffle(dimRange) for c in shuffle(dimRange) ]
nums  = shuffle(range(1,boardDim*boardDim+1))

def generateBoard(): 
    board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]
    squares = boardSize*boardSize
    empties = squares * 3//4
    for p in sample(range(squares),empties):
        board[p//boardSize][p%boardSize] = 0
    return board
