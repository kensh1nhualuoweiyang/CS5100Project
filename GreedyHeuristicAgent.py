import random


valueMapping = {"K":0, "P":1,"N":3,"B":3,"R":5,"Q":9}
CHECKMATE = 1000
STALEMATE = 0


def minMaxMove(state,validMove,maxDepth):
    global nextMove
    nextMove = None
    global moveExpanded 
    moveExpanded= len(validMove)
    minMaxMoveHelper(state,maxDepth,validMove,state.whiteToMove,maxDepth)
    if nextMove is None:
        nextMove = random.choice(validMove)
    return (nextMove,moveExpanded)


def minMaxMoveHelper(state,depth,validMoves,whiteToMove,maxDepth):
    global nextMove
    global moveExpanded
    random.shuffle(validMoves)
    if depth == 0:
        return evaluateBoard(state)    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            state.makeMove(move)
            moveSet = state.getValidMoves()
            moveExpanded += len(moveSet)
            score = minMaxMoveHelper(state,depth-1,moveSet, False,maxDepth)
            if score > maxScore:
                maxScore = score
                if depth == maxDepth:
                    nextMove = move
            state.undoMove()
        return maxScore
    else:
        maxScore = CHECKMATE
        for move in validMoves:
            state.makeMove(move)
            moveSet = state.getValidMoves()
            moveExpanded += len(moveSet)
            score = minMaxMoveHelper(state,depth-1,moveSet, True,maxDepth)
            if score < maxScore:
                maxScore = score
                if depth == maxDepth:
                    nextMove = move
            state.undoMove()
        return maxScore
                
                
    
'''
Greedy Heuristic that evaluate the board base on the current piece
'''
def evaluateBoard(state):
    if state.checkMate:
        if state.whiteToMove:
            return -CHECKMATE
        return CHECKMATE
    elif state.staleMate:
        return 0

    result = 0
    for row in state.board:
        for col in row:
            if col[0] == "w":
                result += valueMapping[col[1]]
            elif col[0] == "b":
                result -= valueMapping[col[1]]
    return result
            
