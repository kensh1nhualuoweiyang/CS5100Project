import pygame as p
import Engine

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
    curren_state = "Playing"
    sqSelected = ()
    playerClicks = []
    possibleMove = state.getValidMoves()
    while curren_state == "Playing":
        for e in p.event.get():
            if e.type == p.QUIT:
                curren_state = "Quit"
            #Utilized for checking purposes
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
               
                if len(playerClicks) == 2:
                    moveMade = False
                    move = Engine.Move(playerClicks[0],playerClicks[1],state.board)
                    for moves in possibleMove:
                        if move == moves:                      
                            state.makeMove(moves)
                            sqSelected = ()
                            playerClicks = []
                            possibleMove = state.getValidMoves()
                            moveMade = True
                            break
                    if not moveMade:
                        playerClicks = [sqSelected]
                if state.checkMate:
                    curren_state = "GAMEOVER"
                    if state.whiteToMove:
                        curren_state = "Black Win"
                    else:
                        curren_state = "White Win"
                elif state.staleMate:
                    curren_state = "Draw"
            elif e.type == p.KEYDOWN:
                state.undoMove()
                possibleMove = state.getValidMoves()


    
        drawGameState(screen,state)
        p.display.flip()
    print(curren_state)


if __name__=="__main__":
    main()