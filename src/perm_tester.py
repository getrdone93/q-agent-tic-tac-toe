#!/usr/bin/python
from common import *

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

def testAgent(stateActValue, initialBoard, machine, permAgent, turn):
    newBoard = initialBoard
    gameOver = False
    while True:
        gameOver = isGameOver(newBoard)
        if gameOver:
            if isWin(newBoard, permAgent):
                global PERM_AGENT_WINS
                PERM_AGENT_WINS += 1
                return 1
            elif isWin(newBoard, machine):
                global Q_AGENT_WINS
                Q_AGENT_WINS += 1
                return 2
            elif isCat(newBoard):
                global CAT_GAMES
                CAT_GAMES += 1
                return 0
            
        if turn == machine:
            newBoard = machineTurn(newBoard, stateActValue, machine, False)
        else:
            actions = getActions(newBoard)
            saveBoard = newBoard
            for act in actions:
                newBoard = invokeAction(act, permAgent, saveBoard)
        turn = getTurn(turn)
        
    return -1

#             if learnNewValues:
#                 while ready != 2:
#                     ready = 0 
#                     resetGlobals()
#                         
#                     print "I have to play with myself, hold on..."
#                     generateGames(stateActValue, stateActFreq, human, machine, 2000000)
#                     
#                     print "Testing the agent against the permutation agent..."
#                     print "testing agent as %s" % (machine)
#                     testAgent(stateActValue, generateBoard(), machine, permAgent, X)
#                     print "Q-AGENT: %d\tPERM_AGENT: %d\tCAT: %d" % (Q_AGENT_WINS, PERM_AGENT_WINS, CAT_GAMES)
#                     
#                     if PERM_AGENT_WINS == 0:
#                         ready += 1
#                     
#                     resetGlobals()
#                     
#                     print "testing agent as %s" % (permAgent)
#                     testAgent(stateActValue, generateBoard(), permAgent, machine, X)
#                     print "Q-AGENT: %d\tPERM_AGENT: %d\tCAT: %d" % (Q_AGENT_WINS, PERM_AGENT_WINS, CAT_GAMES)
#                     
#                     if PERM_AGENT_WINS == 0:
#                         ready += 1
#             
#             if learnNewValues:
#                 print "persisting my learned self to disk..."
#                 fileHandle = open(fileName, "wb")
#                 pickle.dump(stateActValue, fileHandle)
#                 fileHandle.close()
#                 learnNewValues = False