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
    if nextMove is None and len(validMove) > 0:
        nextMove = random.choice(validMove)
    return (nextMove,moveExpanded)

def minMaxMoveHelper(state,depth,validMoves,whiteToMove,maxDepth):
    global nextMove
    global moveExpanded
    random.shuffle(validMoves)
    moveExpanded+=1
    if depth == 0:
        return evaluateBoard(state)    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            state.makeMove(move)
            moveSet = state.getValidMoves()         
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
                

def negaMaxAlphaBeta(state,validMoves,depth):
    global nextMove
    global moveExpanded
    moveExpanded= 0
    nextMove = None
    random.shuffle(validMoves)
    negaMaxHelperWithAlphaBeta(state,validMoves, depth,1 if state.whiteToMove else -1,depth,-CHECKMATE,CHECKMATE)
    if nextMove is None and len(validMoves) > 0:
        nextMove = random.choice(validMoves)
    return (nextMove,moveExpanded)

def negaMaxHelperWithAlphaBeta(state,validMoves,depth,turnMultiplier,maxDepth,alpha,beta):
    global nextMove
    global moveExpanded
    if depth == 0:
        return turnMultiplier * evaluateBoard(state)
    maxScore = -CHECKMATE
    for move in validMoves:
        state.makeMove(move)
        moveSet = state.getValidMoves()
        score = -negaMaxHelperWithAlphaBeta(state,moveSet,depth-1,-turnMultiplier,maxDepth,-beta,-alpha)
        if score > maxScore:
            maxScore = score
            if depth == maxDepth:
                nextMove = move
        state.undoMove()
        moveExpanded+=1
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

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
            
