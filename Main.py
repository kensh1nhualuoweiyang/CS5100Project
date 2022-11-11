import pygame as p
import Engine
import GreedyHeuristicAgent

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGE = {}

def loadImages():
    pieces = ["bB","bK","bN","bP","bQ","bR","wB","wK","wN","wP","wQ","wR"]
    for piece in pieces:
        IMAGE[piece] = p.transform.scale(p.image.load("images/" + piece +".png"),(SQ_SIZE,SQ_SIZE))

def drawBoard(screen,board):
    colors = [p.Color("white"),p.Color("gray")]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            currentColor = colors[(i+j)%2]
            p.draw.rect(screen,currentColor,p.Rect(j*SQ_SIZE,i*SQ_SIZE,SQ_SIZE,SQ_SIZE))
            currentPiece = board[i][j]
            if currentPiece != "--":
                screen.blit(IMAGE[currentPiece],p.Rect(j*SQ_SIZE,i*SQ_SIZE,SQ_SIZE,SQ_SIZE))



def drawGameState(screen,state):
    drawBoard(screen,state.board)


def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    screen.fill(p.Color("white"))
    state = Engine.GameState()
    loadImages()
    while not state.checkMate or not state.staleMate:
        agentMove = GreedyHeuristicAgent.minMaxMove(state,state.getValidMoves(),3)
        state.makeMove(agentMove)     
        drawGameState(screen,state)
        p.display.flip()
    if state.checkMate():
        if state.whiteToMove:
            print("Black Win")
        else:
            print("White Win")
    else:
        print("Draw")


if __name__=="__main__":
    main()