import random


class Agent():
    def __init__(self, depth, alphaBeta=False, positioning=False, monteCarlo=False):
        self.depth = depth
        self.alphaBeta = alphaBeta
        self.positioning = positioning
        self.monteCarlo = monteCarlo
        self.valueMapping = {"K": 0, "P": 1, "N": 3, "B": 3, "R": 5, "Q": 9}
        self.moveExpanded = 0
        self.nextMove = None
        self.knightScore = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 2, 2, 2, 2, 2, 2, 1],
                            [1, 2, 3, 3, 3, 3, 2, 1],
                            [1, 2, 3, 4, 4, 3, 2, 1],
                            [1, 2, 3, 4, 4, 3, 2, 1],
                            [1, 2, 3, 3, 3, 3, 2, 1],
                            [1, 2, 2, 2, 2, 2, 2, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1]]

        self.whitePawnScore = [[8, 8, 8, 8, 8, 8, 8, 8],
                               [8, 8, 8, 8, 8, 8, 8, 8],
                               [5, 6, 6, 7, 7, 6, 6, 5],
                               [2, 3, 3, 5, 5, 3, 3, 2],
                               [1, 2, 3, 4, 4, 3, 2, 1],
                               [1, 1, 2, 3, 3, 2, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1],
                               [0, 0, 0, 0, 0, 0, 0, 0]]

        self.blackPawnScore = [[0, 0, 0, 0, 0, 0, 0, 0],
                               [1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 2, 3, 3, 2, 1, 1],
                               [1, 2, 3, 4, 4, 3, 2, 1],
                               [2, 3, 3, 5, 5, 3, 3, 2],
                               [5, 6, 6, 7, 7, 6, 6, 5],
                               [8, 8, 8, 8, 8, 8, 8, 8],
                               [8, 8, 8, 8, 8, 8, 8, 8]]

        self.bishopScore = [[4, 3, 2, 1, 1, 2, 3, 4],
                            [3, 4, 3, 2, 2, 3, 4, 3],
                            [2, 3, 4, 3, 3, 4, 3, 2],
                            [1, 2, 3, 4, 4, 3, 2, 1],
                            [1, 2, 3, 4, 4, 3, 2, 1],
                            [2, 3, 4, 3, 3, 4, 3, 2],
                            [3, 4, 3, 2, 2, 3, 4, 3],
                            [4, 3, 2, 1, 1, 2, 3, 4]]

        self.rookScore = [[4, 3, 4, 4, 4, 4, 3, 4],
                          [4, 4, 4, 4, 4, 4, 4, 4],
                          [1, 1, 2, 3, 3, 2, 1, 1],
                          [1, 2, 3, 4, 4, 3, 2, 1],
                          [1, 2, 3, 4, 4, 3, 2, 1],
                          [1, 1, 2, 3, 3, 2, 1, 1],
                          [4, 4, 4, 4, 4, 4, 4, 4],
                          [4, 3, 4, 4, 4, 4, 3, 4]]

        self.queenScore = [[1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 2, 3, 3, 3, 1, 1, 1],
                           [1, 4, 3, 3, 3, 4, 2, 1],
                           [1, 2, 3, 3, 3, 2, 2, 1],
                           [1, 2, 3, 3, 3, 2, 2, 1],
                           [1, 4, 3, 3, 3, 4, 2, 1],
                           [1, 2, 3, 3, 3, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1]]

        self.piecePositionScore = {"N": self.knightScore, "Q": self.queenScore, "R": self.rookScore,
                                   "B": self.bishopScore, "bP": self.blackPawnScore, "wP": self.whitePawnScore}

        self.CHECKMATE = 1000
        self.STALEMATE = 0

    def __str__(self):
        return "Agent with depth {} {} ".format(self.depth, "with alpha beta" if self.alphaBeta else "", "with position evaluation" if self.positioning else "")

    def makeMove(self, state):
        if self.alphaBeta:
            return self.negaMaxAlphaBeta(state, state.getValidMoves(), self.depth)
        else:
            return self.minMaxMove(state, state.getValidMoves(), self.depth)

    def minMaxMove(self, state, validMove, maxDepth):
        self.nextMove = None
        self.minMaxMoveHelper(state, maxDepth, validMove, state.whiteToMove, maxDepth)
        return self.nextMove

    def minMaxMoveHelper(self, state, depth, validMoves, whiteToMove, maxDepth):
        random.shuffle(validMoves)
        if depth == 0:
            return self.evaluateBoard(state) if not self.positioning else self.evaluateBoardWithPosition(state)
        self.moveExpanded += len(validMoves)
        if whiteToMove:
            maxScore = -self.CHECKMATE
            for move in validMoves:
                state.makeMove(move)
                moveSet = state.getValidMoves()
                score = self.minMaxMoveHelper(state, depth - 1, moveSet, False, maxDepth)
                if score > maxScore:
                    maxScore = score
                    if depth == maxDepth:
                        self.nextMove = move
                state.undoMove()
            return maxScore
        else:
            maxScore = self.CHECKMATE
            for move in validMoves:
                state.makeMove(move)
                moveSet = state.getValidMoves()
                score = self.minMaxMoveHelper(state, depth - 1, moveSet, True, maxDepth)
                if score < maxScore:
                    maxScore = score
                    if depth == maxDepth:
                        self.nextMove = move
                state.undoMove()
            return maxScore

    def negaMaxAlphaBeta(self, state, validMoves, depth):
        self.nextMove = None
        random.shuffle(validMoves)
        self.negaMaxHelperWithAlphaBeta(state, validMoves, depth, 1 if state.whiteToMove else -1, depth,
                                        -self.CHECKMATE, self.CHECKMATE)
        return self.nextMove

    def negaMaxHelperWithAlphaBeta(self, state, validMoves, depth, turnMultiplier, maxDepth, alpha, beta):
        if depth == 0:
            return turnMultiplier * (
                self.evaluateBoardWithPosition(state) if self.positioning else self.evaluateBoard(state))
        maxScore = -self.CHECKMATE
        for move in validMoves:
            state.makeMove(move)
            moveSet = state.getValidMoves()
            score = -self.negaMaxHelperWithAlphaBeta(state, moveSet, depth - 1, -turnMultiplier, maxDepth, -beta,
                                                     -alpha)
            if score > maxScore:
                maxScore = score
                if depth == maxDepth:
                    self.nextMove = move
            state.undoMove()
            self.moveExpanded += 1
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break
        return maxScore

    def evaluateBoard(self, state):
        if state.checkMate:
            if state.whiteToMove:
                return -self.CHECKMATE
            return self.CHECKMATE
        elif state.staleMate:
            return 0

        result = 0
        for row in state.board:
            for col in row:
                if col[0] == "w":
                    result += self.valueMapping[col[1]]
                elif col[0] == "b":
                    result -= self.valueMapping[col[1]]
        return result

    def evaluateBoardWithPosition(self, state):
        if state.checkMate:
            if state.whiteToMove:
                return -self.CHECKMATE
            return self.CHECKMATE
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
                            positionScore = self.piecePositionScore[piece][row][col]
                        else:
                            positionScore = self.piecePositionScore[piece[1]][row][col]
                    if piece[0] == "w":
                        result += self.valueMapping[col[1]] + positionScore * 0.1
                    elif piece[0] == "b":
                        result -= self.valueMapping[col[1]] + positionScore * 0.1

        return result
