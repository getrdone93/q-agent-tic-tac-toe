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
                #print "perm agent wins"
                global PERM_AGENT_WINS
                PERM_AGENT_WINS += 1
                return 1
            elif isWin(newBoard, machine):
                #print "q agent wins"
                global Q_AGENT_WINS
                Q_AGENT_WINS += 1
                return 2
            elif isCat(newBoard):
                #print "cat"
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