#!/usr/bin/python
from math import ceil
from random import randint
import pickle

BOARD_LEN = 9
X = 'x'
O = 'o'
WIN_REWARD = 99
CAT_REWARD = .5
NON_TERM_REWARD = 0
LOSS_REWARD = -99

EXPLORE_MAX = 5 #deprecated

#None space is unoccupied
#x means x is in space
#o means o is in space
def generateBoard():
    return tuple([None for n in range(BOARD_LEN)])

def invokeAction(index, ele, board):
    result = list(board[:])
    result[index] = ele
    return tuple(result)

def getTurn(turn):
    return X if turn == O else O

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

def getActions(board):
    result = []
    if board != () and not isGameOver(board):
        for idx, ele in enumerate(board):
            if ele == None:
                result.append(idx)
    return result

def getAllBoards(board, turn, allBoards):
    boardActions = getActions(board)
    while boardActions != []:
        root = invokeAction(boardActions.pop(), turn, board)
        allBoards.add(root)
        if isGameOver(root):
            continue
        getAllBoards(root, getTurn(turn), allBoards)
 
def getStateAction(allBoards):
    result = {}
    for board in allBoards:
        if isGameOver(board):
            result[(board, None)] = 0
            result[(board, None)] = 0
        else:
            actions = getActions(board)
            for act in actions:
                result[(board, act)] = 0
                result[(board, act)] = 0
    return result

def stepSizeFunc(n):
    return 60 / float((59 + (1 if n == 0 else n)))

def getMinMaxByBoard(board, dictionary, minMax):
    actions = getActions(board);
    values = set()
    for action in actions:
        values.add(dictionary[(board, action)])
    
    return minMax(values)         

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

def getPreviousAction(prevBoard, currentBoard):
    #the index that differs is the previous action
    #that action was invoked on b1 which resulted in b2
    if prevBoard == None:
        return None
    for index in enumerate(currentBoard):
        if index[1] != prevBoard[index[0]]:
            return index[0]

def getAction(prevBoard, currentBoard):
    result = None
    if prevBoard != None:
        for idx, ele in enumerate(prevBoard):
            if ele != currentBoard[idx]:
                result = idx
                break
    return result

def output(ele, ind):
    return ' ' + (str(ind) if ele == None else str(ele)) + ' '

def printBoard(board):
    print '\n%s|%s|%s' % (output(board[0], 0), output(board[1], 1), output(board[2], 2))
    print '-' * 11
    print '%s|%s|%s' % (output(board[3], 3), output(board[4], 4), output(board[5], 5))
    print '-' * 11
    print '%s|%s|%s\n' % (output(board[6], 6), output(board[7], 7), output(board[8], 8))

def getInput(actions):
    inputValid = False
    usrAct = None
    while not inputValid:
        usrAct = raw_input("Enter move: ")
        usrAct = int(usrAct)
        if usrAct in set(actions):
            inputValid = True
        else:
            print "Invalid action. Valid actions are: " + str(actions)
    return usrAct
            
def humanTurn(board, human):        
    usrAct = getInput(getActions(board))
    return invokeAction(usrAct, human, board)

def getBestMove(board, stateActValue, minMax):
    actions = getActions(board)
    actionVals = {}
    result = None
    for act in actions:
        actionVals[stateActValue[(board, act)]] = act

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
        if randint(0, 99) in range(0, 12): #12 percent chance, good thing randint is inclusive and range is not (dat's sarcastic BWOH)
            possibles = getActions(board)
            action = possibles[randint(0, len(possibles) - 1)]
        else:
            action = getBestMove(board, stateActValue, min if machine == O else max)
    else:
        action = getBestMove(board, stateActValue, min if machine == O else max)
        
    return invokeAction(action, machine, board) 

def generateGames(stateActValue, stateActFreq, machine1, machine2, numTimes):
    games = []
    for i in range(0, numTimes):
        if i % 10000 == 0:
            print "I'm %f percent done playing with myself" % ((float(i) / numTimes) * 100)
        playGame(stateActValue, stateActFreq, machine1, machine2, True)
    return games

def play(stateActValue, human, machine):
    return playGame(stateActValue, human, machine, False)  

def learn(currentBoard, nextBoard, nextReward, stateActValue, stateActFreq, discount, turn):
    currentAction = getAction(currentBoard, nextBoard)
    if nextBoard != () and isGameOver(nextBoard):
        stateActValue[(currentBoard, currentAction)] += nextReward
        
    if currentBoard != None and currentAction != None:
        stateActFreq[(currentBoard, currentAction)] += 1
        
        minMax = rewardFunction(nextBoard) if isGameOver(nextBoard) else getMinMaxByBoard(nextBoard, stateActValue, max if turn == O else min)
        stateActValue[(currentBoard, currentAction)] = (stateActValue[(currentBoard, currentAction)] 
                                            + stepSizeFunc(stateActFreq[(currentBoard, currentAction)]) 
                                            * ((nextReward + discount * minMax)
                                               - stateActValue[(currentBoard, currentAction)]))
       
def playGame(stateActValue, stateActFreq, human, machine, learning):
    board = generateBoard()
    turn = human if human == X else machine 
    if not learning:
        print "Initial board: "
    gameOver = False;
    while not gameOver:
        if not learning:
            printBoard(board)
        if turn == human:
            if learning:
                newBoard = machineTurn(board, stateActValue, human, learning)
            else:
                newBoard = humanTurn(board, human)
        else:
            newBoard = machineTurn(board, stateActValue, machine, learning)
            if not learning:
                print "Machine move: " + str(getPreviousAction(board, newBoard))
         
        if learning:
            learn(board, newBoard, rewardFunction(newBoard), stateActValue, stateActFreq, 1, turn)
        board = newBoard
        gameOver = isGameOver(board)
        if gameOver:
            if isWin(board, human):
                if not learning:
                    print "Human wins!"
            elif isWin(board, machine):
                if not learning:
                    print "Machine wins!"
            elif isCat(board):
                if not learning:
                    print "Draw!"
            if not learning:
                printBoard(board)
        
        turn = getTurn(turn)

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

PERM_AGENT_WINS = 0
Q_AGENT_WINS = 0
CAT_GAMES = 0

def resetGlobals():
    global Q_AGENT_WINS
    Q_AGENT_WINS = 0
    
    global PERM_AGENT_WINS
    PERM_AGENT_WINS = 0
    
    global CAT_GAMES
    CAT_GAMES = 0
        
def main():
        playAgain = True
        stateActValue = None
        stateActFreq = None
        fileName = "state.dat"
        learnNewValues = False
        try:
            handle = open(fileName, "rb")
        except IOError:
            print "have to learn new values, file isnt there"
            learnNewValues = True
        else:
            stateActValue = pickle.load(handle)
        
        while playAgain:
            human = raw_input("Do you want to be x or o? ").lower()
            machine = getTurn(human)
            ready = 0
            permAgent = human
            if learnNewValues:
                while ready != 2:
                    ready = 0 
                    resetGlobals()
                    emptyBoard = generateBoard()
                    allBoards = set([])
                    allBoards.add(emptyBoard)
                    getAllBoards(emptyBoard, X, allBoards)
                    stateActValue = getStateAction(allBoards)
                    stateActFreq = getStateAction(allBoards)
                    
                    print "I have to play with myself, hold on..."
                    generateGames(stateActValue, stateActFreq, human, machine, 2000000)
                    
                    print "Testing the agent against the permutation agent..."
                    print "testing agent as %s" % (machine)
                    testAgent(stateActValue, generateBoard(), machine, permAgent, X)
                    print "Q-AGENT: %d\tPERM_AGENT: %d\tCAT: %d" % (Q_AGENT_WINS, PERM_AGENT_WINS, CAT_GAMES)
                    
                    if PERM_AGENT_WINS == 0:
                        ready += 1
                    
                    resetGlobals()
                    
                    print "testing agent as %s" % (permAgent)
                    testAgent(stateActValue, generateBoard(), permAgent, machine, X)
                    print "Q-AGENT: %d\tPERM_AGENT: %d\tCAT: %d" % (Q_AGENT_WINS, PERM_AGENT_WINS, CAT_GAMES)
                    
                    if PERM_AGENT_WINS == 0:
                        ready += 1
            
            if learnNewValues:
                print "persisting my learned self to disk..."
                fileHandle = open(fileName, "wb")
                pickle.dump(stateActValue, fileHandle)
                fileHandle.close()
                learnNewValues = False
            
            print "\nPlay!\n"
            playGame(stateActValue, stateActFreq, human, machine, False)
            playAgainInput = raw_input("Do you want to play again (y, n)? ").lower()
            playAgain = True if playAgainInput == 'y' else False
            if playAgain:
                sameSettingsInput = raw_input("Would you like to keep the same settings(i.e. play the same agent again?) (y, n)? ").lower()
                sameSettings = True if sameSettingsInput == 'y' else False 
main()