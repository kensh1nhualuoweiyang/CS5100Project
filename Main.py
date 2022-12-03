import math
import random

import pygame as p
import Engine
from GreedyHeuristicAgent import Agent
import time

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGE = {}


def loadImages():
    pieces = ["bB", "bK", "bN", "bP", "bQ", "bR", "wB", "wK", "wN", "wP", "wQ", "wR"]
    for piece in pieces:
        IMAGE[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def drawBoard(screen, board):
    colors = [p.Color("white"), p.Color("gray")]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            currentColor = colors[(i + j) % 2]
            p.draw.rect(screen, currentColor, p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            currentPiece = board[i][j]
            if currentPiece != "--":
                screen.blit(IMAGE[currentPiece], p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawGameState(screen, state):
    drawBoard(screen, state.board)
def playChess(state,agentOne,agentTwo):
    totalMove = 0
    startTime = time.time()
    while not state.checkMate or not state.staleMate:
        if state.whiteToMove:
            agentOneMove = agentOne.makeMove(state)
            if agentOneMove is not None:
                state.makeMove(agentOneMove)
            else:
                if len(state.getValidMoves()) == 0:
                    break
                state.makeMove(random.choice(state.getValidMoves()))
        else:
            agentTwoMove = agentTwo.makeMove(state)
            if agentTwoMove is not None:
                state.makeMove(agentTwoMove)
            else:
                if len(state.getValidMoves()) == 0:
                    break
                state.makeMove(random.choice(state.getValidMoves()))

        totalMove += 1
        print("{} Move Made".format(totalMove))

        # drawGameState(screen, state)
        # p.display.flip()
    endTime = time.time()
    f = open("GameResult.md", "a")
    totalTime = math.floor((endTime - startTime) / 60)
    if state.checkMate:
        if state.whiteToMove:
            f.write(
                "\n{}\n{} victory against {} \nAgent Two Move Expanded: {} \nAgent One Move Expanded: {}\n".format(
                    "_" * 70,
                    agentTwo,
                    agentOne,
                    agentTwo.moveExpanded,
                    agentOne.moveExpanded))
        else:
            f.write(
                "\n{}\n{} victory against {} \nAgent One Move Expanded: {} \nAgent Two Move Expanded: {}\n".format(
                    "_" * 70,
                    agentOne,
                    agentTwo,
                    agentOne.moveExpanded,
                    agentTwo.moveExpanded))
    elif state.staleMate:
        f.write("\n{}\n{} draw against {} \nAgent One Move Expanded: {} \nAgent Two Move Expanded: {}\n".format("_" * 70,
                                                                                                            agentOne,
                                                                                                            agentTwo,
                                                                                                            agentOne.moveExpanded,
                                                                                                            agentTwo.moveExpanded))

    f.write("Time Elapsed: {} minute\n{}".format(totalTime, "_" * 70))
    f.close()

def gameSetUp(agentOne,agentTwo):
    for i in range(5):
        state = Engine.GameState()
        playChess(state, agentOne, agentTwo)
def main():
    #p.init()
    #screen = p.display.set_mode((WIDTH, HEIGHT))
    #screen.fill(p.Color("white"))

    #loadImages()
    """
    gameSetUp(Agent(3, alphaBeta=True, positioning=True), Agent(2, alphaBeta=True))
    gameSetUp(Agent(3, alphaBeta=True, positioning=True), Agent(2, alphaBeta=True,positioning=True))
    gameSetUp(Agent(3, alphaBeta=True,positioning=True), Agent(3,alphaBeta=True))
    gameSetUp(Agent(3, alphaBeta=True, positioning=True), Agent(3, alphaBeta=True,positioning=True))
    gameSetUp(Agent(3, alphaBeta=True), Agent(4, alphaBeta=True))
    gameSetUp(Agent(3, alphaBeta=True,positioning=True), Agent(4,alphaBeta=True))
    gameSetUp(Agent(3, alphaBeta=True, positioning=True), Agent(4, alphaBeta=True,positioning=True))
    """


    gameSetUp(Agent(3, alphaBeta=True), Agent(4, alphaBeta=True, positioning=True))




if __name__ == "__main__":
    main()
