import numpy as np

class GameState():
    def __init__(self):
        '''
        Represent the 8x8 chess board, first character is their color
        and second character is their type,
        -- represents the initial empty space with no pieces.
        '''
        self.board = np.array(
            [["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]],dtype=object,
            )
        self.moveFunctions = {"P":self.getPawnMoves,"R":self.getRookMoves,"N":self.getKnightMoves,"B":self.getBishopMoves
        ,"Q":self.getQueenMoves,"K":self.getKingMoves}
        self.whiteToMove = True

    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        pass
    
    def getAllPossibleMoves(self):
        moves = []
        count = 0
        for i in range(8):
            for j in range(8):
                color = self.board[i][j][0]
                piece = self.board[i][j][1]
                
                if (color == "w" and self.whiteToMove) or (color == "b" and not self.whiteToMove):
                    self.moveFunctions[piece](i,j,moves)
                    count+=1
                if count >= 16:
                    return moves
        return moves

    def getPawnMoves(self,row,col,moves):
        if self.whiteToMove:
            if row -1 >= 0:
                if self.board[row-1][col] == "--":
                    moves.append(Move((row,col),(row-1,col),self.board))
                    if row == 6 and self.board[row-2][col] == "--":
                        moves.append(Move((row,col),(row-2,col),self.board))
            if col-1 >= 0:
                if self.board[row-1][col-1][0] == "b":
                    moves.append(Move((row,col),(row-1,col-1),self.board))
            if col+1 <= 7:
                if self.board[row - 1][col +1][0] == "b":
                    moves.append(Move((row,col),(row-1,col+1),self.board))

        else:
            if row + 1 <= 7:
                if self.board[row+1][col] == "--":
                    moves.append(Move((row,col),(row+1,col),self.board))
                    if row == 1 and self.board[row+2][col] == "--":
                        moves.append(Move((row,col),(row+2,col),self.board))
            if col-1 >= 0:
                if self.board[row+1][col-1][0] == "w":
                    moves.append(Move((row,col),(row+1,col-1),self.board))
            if col+1 <= 7:
                if self.board[row + 1][col +1][0] == "w":
                    moves.append(Move((row,col),(row+1,col+1),self.board))
    
    def rookAndBishopMove(self,row,col,moves,direction):
        enemyColor = "b" if self.whiteToMove else "w"
        for d in direction:
            for i in range(1,8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--" :
                        moves.append(Move((row,col),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row,col),(endRow,endCol),self.board))
                        break
                    else:
                        break
                else:
                    break
    def knightAndKingMove(self,row,col,moves,direction):
        enemyColor = "b" if self.whiteToMove else "w"
        for d in direction:
            endRow = row+d[0]
            endCol = col+d[1]
            if 0 <= endRow <8 and 0<= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor or endPiece == "--":
                    moves.append(Move((row,col),(endRow,endCol),self.board))
                    
    def getRookMoves(self,row,col,moves):
        direction = ((-1,0),(0,-1),(1,0),(0,1))
        self.rookAndBishopMove(row,col,moves,direction)
    
    def getBishopMoves(self,row,col,moves):
        direction = ((-1,-1),(-1,1),(1,1),(1,-1))
        self.rookAndBishopMove(row,col,moves,direction)

    def getQueenMoves(self,row,col,moves):
        self.getBishopMoves(row,col,moves)
        self.getRookMoves(row,col,moves)

    

    def getKingMoves(self,row,col,moves):
        direction = ((-1,-1),(-1,0),(-1,1),(1,1),(0,-1),(0,1),(1,-1),(1,0))
        self.knightAndKingMove(row,col,moves,direction)

    def getKnightMoves(self,row,col,moves):
        direcitons = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        self.knightAndKingMove(row,col,moves,direcitons)


class Move():
    def __init__(self,startSq,endSq,board) :
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    
    def __eq__(self, object) -> bool:
        if isinstance(object,Move):
            return object.moveID == self.moveID