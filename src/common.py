#!/usr/bin/python
from random import randint
import pickle

BOARD_LEN = 9
X = 'x'
O = 'o'
WIN_REWARD = 99
CAT_REWARD = .5
NON_TERM_REWARD = 0
LOSS_REWARD = -99
STATE_ACT_VALUE_FILE = "state.dat"

def addToFrequency(tup, value):
    return (tup[0], tup[1] + value)

def addToValue(tup, value):
    return (tup[0] + value, tup[1])

def loadStateActValueFile():
    stateActValue = None
    try:
        handle = open(STATE_ACT_VALUE_FILE, "rb")
    except IOError:
        print "ERROR: %s file does not exist." % (STATE_ACT_VALUE_FILE)
    else:
        stateActValue = pickle.load(handle)
    
    return stateActValue

def writeStateActValueFile(stateActValue):
    try:
        handle = open(STATE_ACT_VALUE_FILE, "wb")
    except IOError:
        print "ERROR: when opening %s for write" % (STATE_ACT_VALUE_FILE)
    else:
        pickle.dump(stateActValue, handle)
        

def getBestMove(board, stateActValue, minMax):
    actions = getActions(board)
    actionVals = {}
    result = None
    for act in actions:
        actionVals[stateActValue[(board, act)][0]] = act

    if len(actionVals) == 1:
        #all of the actions are equal so choose at random
        result = actions[randint(0, len(actions) - 1)] 
    else:
        #hashed by value of action so return min/max key
        result = actionVals[minMax(actionVals.keys())]
               
    return result

def machineTurn(board, stateActValue, machine, learning):
    action = None
    if learning:
        if randint(0, 99) in range(0, 12): #12 percent chance to move randomly
            possibles = getActions(board)
            action = possibles[randint(0, len(possibles) - 1)]
        else:
            action = getBestMove(board, stateActValue, min if machine == O else max)
    else:
        action = getBestMove(board, stateActValue, min if machine == O else max)
        
    return invokeAction(action, machine, board) 

def getAction(prevBoard, currentBoard):
    result = None
    if prevBoard != None:
        for idx, ele in enumerate(prevBoard):
            if ele != currentBoard[idx]:
                result = idx
                break
    return result

def rewardFunction(board):
    if board == ():
        return NON_TERM_REWARD
    elif isWin(board, X):
        return WIN_REWARD
    elif isWin(board, O):
        return LOSS_REWARD
    elif isCat(board):
        return CAT_REWARD
    else:
        return NON_TERM_REWARD

def getMinMaxByBoard(board, dictionary, minMax):
    actions = getActions(board);
    values = set()
    for action in actions:
        values.add(dictionary[(board, action)][0])
    
    return minMax(values)  

def getTurn(turn):
    return X if turn == O else O

def invokeAction(index, ele, board):
    result = list(board[:])
    result[index] = ele
    return tuple(result)

def getActions(board):
    result = []
    if board != () and not isGameOver(board):
        for idx, ele in enumerate(board):
            if ele == None:
                result.append(idx)
    return result

def isCat(board):
    return len([ele for ele in board if ele != None]) == BOARD_LEN

def isWin(board, char):
    return ((board[0] == char and board[1] == char and board[2] == char)
    or (board[3] == char and board[4] == char and board[5] == char)
    or (board[6] == char and board[7] == char and board[8] == char)
    #top to bottom wins
    or  (board[0] == char and board[3] == char and board[6] == char)
    or  (board[1] == char and board[4] == char and board[7] == char)
    or  (board[2] == char and board[5] == char and board[8] == char)
    #diagonal wins
    or  (board[0] == char and board[4] == char and board[8] == char)
    or  (board[2] == char and board[4] == char and board[6] == char))

def isGameOver(board):
    return isCat(board) or isWin(board, X) or isWin(board, O)

#None space is unoccupied
#x means x is in space
#o means o is in space
def generateBoard():
    return tuple([None for n in range(BOARD_LEN)])