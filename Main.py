import pygame as p
import Engine
import GreedyHeuristicAgent

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGE = {}
'''
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

'''




def main():
    #p.init()
    #screen = p.display.set_mode((WIDTH,HEIGHT))
    #screen.fill(p.Color("white"))
    state = Engine.GameState()
    #loadImages()
    whiteMoveExpanded = 0
    blackMoveExpanded = 0
    agentOneMethod ="GreedyHeuristicAgent"
    agentTwoMethod = "GreedyHeuristicAgent"
    agentOneDepth = 3
    agentTwoDepth = 2
    whiteMoveCount = 0
    blackMoveCount = 0
    while not state.checkMate or not state.staleMate:
        if state.whiteToMove:
            agentOne,moveExpanded= GreedyHeuristicAgent.minMaxMove(state,state.getValidMoves(),agentOneDepth)
            state.makeMove(agentOne)
            whiteMoveExpanded += moveExpanded
            whiteMoveCount+=1
            print("Current White Move Count = ",whiteMoveCount)    
            
        else:
            agentTwo,moveExpanded = GreedyHeuristicAgent.minMaxMove(state,state.getValidMoves(),agentTwoDepth)
            state.makeMove(agentTwo)     
            blackMoveExpanded += moveExpanded
            blackMoveCount+=1
            print("Current Black Move Count = ",blackMoveCount)    
            


        #drawGameState(screen,state)
        #p.display.flip()
    f = open("GameResult.md","a")
    if state.checkMate:
        if state.whiteToMove:
            f.write("Black: {} with depth {} won against {} with Depth {}, total state expanded = {} for black and {} for white\n".format(
            agentTwoMethod,agentTwoDepth,agentOneMethod,agentOneDepth,blackMoveExpanded,whiteMoveExpanded))
        else:
            f.write("White: {} with depth {} won against {} with Depth {}, total state expanded = {} for White and {} for Black\n".format(
            agentOneMethod,agentOneDepth,agentTwoMethod,agentTwoDepth,whiteMoveExpanded,blackMoveExpanded))
    else:
        f.write("{} with depth {} draw against {} with Depth {}, total state expanded = {} for white and {} for black\n".format(agentOneMethod,agentOneDepth,agentTwoMethod,agentTwoDepth,
        whiteMoveExpanded,blackMoveExpanded))
    f.close()
if __name__=="__main__":
    main()
    main()