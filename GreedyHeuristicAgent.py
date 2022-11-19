import random


valueMapping = {"K":0, "P":1,"N":3,"B":3,"R":5,"Q":9}

knightScore = [[1,1,1,1,1,1,1,1],
                [1,2,2,2,2,2,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,2,2,2,2,2,1],
                [1,1,1,1,1,1,1,1]]

whitePawnScore = [[8,8,8,8,8,8,8,8],
                  [8,8,8,8,8,8,8,8],
                  [5,6,6,7,7,6,6,5],
                  [2,3,3,5,5,3,3,2],
                  [1,2,3,4,4,3,2,1],
                  [1,1,2,3,3,2,1,1],
                  [1,1,1,1,1,1,1,1],
                  [0,0,0,0,0,0,0,0]]
blackPawnScore = [[0,0,0,0,0,0,0,0],
                  [1,1,1,1,1,1,1,1],
                  [1,1,2,3,3,2,1,1],
                  [1,2,3,4,4,3,2,1],
                  [2,3,3,5,5,3,3,2],
                  [5,6,6,7,7,6,6,5],
                  [8,8,8,8,8,8,8,8],
                  [8,8,8,8,8,8,8,8],]
bishopScore = [[4,3,2,1,1,2,3,4],
                [3,4,3,2,2,3,4,3],
                [2,3,4,3,3,4,3,2],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [2,3,4,3,3,4,3,2],
                [3,4,3,2,2,3,4,3],
                [4,3,2,1,1,2,3,4]]
rookScore =[[4,3,4,4,4,4,3,4],
            [4,4,4,4,4,4,4,4],
            [1,1,2,3,3,2,1,1],
            [1,2,3,4,4,3,2,1],
            [1,2,3,4,4,3,2,1],
            [1,1,2,3,3,2,1,1],
            [4,4,4,4,4,4,4,4],
            [4,3,4,4,4,4,3,4]]

queenScore =[[1,1,1,1,1,1,1,1],
             [1,2,3,3,3,1,1,1],
             [1,4,3,3,3,4,2,1],
             [1,2,3,3,3,2,2,1],
             [1,2,3,3,3,2,2,1],
             [1,4,3,3,3,4,2,1],
             [1,2,3,3,3,1,1,1],
             [1,1,1,1,1,1,1,1]]




piecePositionScore = {"N":knightScore,"Q":queenScore,"R":rookScore,"B":bishopScore,"bP":blackPawnScore,"wP":whitePawnScore}

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


def evaluateBoardWithPosition(state):
    if state.checkMate:
        if state.whiteToMove:
            return -CHECKMATE
        return CHECKMATE
    elif state.staleMate:
        return 0

    result = 0
    for row in range(len(state.board)):
        for col in range(len(state.board[row])):
            piece = state.board[row][col]
            if piece != "--":
                positionScore = 0
                if piece[1] != "K":
                    if piece[1] == "P":
                        positionScore = piecePositionScore[piece][row][col]
                    else:
                        positionScore = piecePositionScore[piece[1]][row][col]
                if piece[0] == "w":
                    result += valueMapping[col[1]] + positionScore * 0.1
                elif piece[0] == "b":
                    result -= valueMapping[col[1]] + positionScore * 0.1

    return result
