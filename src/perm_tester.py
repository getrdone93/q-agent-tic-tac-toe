#!/usr/bin/python
from src.common import generateBoard, X, isGameOver, isWin, isCat, machineTurn, \
    getActions, getTurn, invokeAction

def resetGlobals():
    global Q_AGENT_WINS
    Q_AGENT_WINS = 0
    
    global PERM_AGENT_WINS
    PERM_AGENT_WINS = 0
    
    global CAT_GAMES
    CAT_GAMES = 0

PERM_AGENT_WINS = 0
Q_AGENT_WINS = 0
CAT_GAMES = 0

def testQAgent(stateActValue, machine, permAgent):
    testAgent(stateActValue, generateBoard(), machine, permAgent, X)
    print "Q-Agent as %s -> Q-Agent: %d\tPermutation Agent: %d\tCat: %d" % (machine, Q_AGENT_WINS, PERM_AGENT_WINS, CAT_GAMES)
    return PERM_AGENT_WINS > 0

def testAgent(stateActValue, initialBoard, machine, permAgent, turn):
    newBoard = initialBoard
    gameOver = False
    while not gameOver:
        gameOver = isGameOver(newBoard)
        if gameOver:
            if isWin(newBoard, permAgent):
                global PERM_AGENT_WINS
                PERM_AGENT_WINS += 1
            elif isWin(newBoard, machine):
                global Q_AGENT_WINS
                Q_AGENT_WINS += 1
            elif isCat(newBoard):
                global CAT_GAMES
                CAT_GAMES += 1
        else:
            if turn == machine:
                newBoard = machineTurn(newBoard, stateActValue, machine, False)
            else:
                actions = getActions(newBoard)
                saveBoard = newBoard
                changeTurn = getTurn(turn)
                for act in actions:
                    newBoard = invokeAction(act, permAgent, saveBoard)
                    testAgent(stateActValue, newBoard, machine, permAgent, changeTurn)
            turn = getTurn(turn)