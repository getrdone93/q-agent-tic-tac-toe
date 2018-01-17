#!/usr/bin/python
from math import ceil
from random import randint

BOARD_LEN = 9
X = 'x'
O = 'o'
WIN_REWARD = 1
CAT_REWARD = .5
NON_TERM_REWARD = 0
LOSS_REWARD = -1

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

def getAllBoardsAndPaths(board, turn, allBoards, path, allPaths):
    boardActions = getActions(board)
    while boardActions != []:
        root = invokeAction(boardActions.pop(), turn, board)
        allBoards.add(root)
        if isGameOver(root):
            #board represents a finished game so other player can't go
            #thus no recursive call needs to be made
            #so copy path up to this point and append winning board
            pathCopy = path[:]
            pathCopy.append(root)
            allPaths.add(tuple(tuple(b) for b in pathCopy))
            continue
        getAllBoardsAndPaths(root, getTurn(turn), allBoards, path + [list(root)], allPaths)
 
def getNonTerminalBoards(allBoards):
    return tuple([board for board in allBoards if not isGameOver(board)]) 
        
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

def getMinByBoard(board, dictionary):
    return min([dictionary[key] for key in dictionary if key[0] == board])

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

def explorationFunc(u, n):
    if n < EXPLORE_MAX:
        return WIN_REWARD #return best possible reward obtainable in any state
    return u    

#deprecated
def getBestAction(board, stateActFreq, stateActValue, player):
    actions = getActions(board)
    maxVal = -float("inf")
    result = None
    for act in actions:
        tempVal = explorationFunc(stateActValue[(board, act, player)], stateActFreq[(board, act, player)])
        if maxVal < tempVal:
            maxVal = tempVal
            result = act
    return result

def getPaths(allPaths, timeUb):
    #can learn at about 6000 paths / minute or 2% of space
    result = set([])
    if timeUb < 0:
        return allPaths
    else:
        apList = list(allPaths)
        numBlocks = ceil(float(timeUb) * 6000) #block size is 6000
        size = 0
        while size < numBlocks:
            result.add(apList[randint(0, len(apList) - 1)])
            size += 1
    return result    

def updateRewards(observedRewards, cutoff, reward):
    for ind, entry in enumerate(observedRewards):
        if ind < cutoff:
            for key in entry:
                entry[key] += reward

def getAction(prevBoard, currentBoard):
    result = None
    if prevBoard != None:
        for idx, ele in enumerate(prevBoard):
            if ele != currentBoard[idx]:
                result = idx
                break
    return result

def learn(currentBoard, nextBoard, nextReward, stateActValue, stateActFreq, discount, turn):
    currentAction = getAction(currentBoard, nextBoard)
    if nextBoard != () and isGameOver(nextBoard):
        stateActValue[(currentBoard, currentAction)] += nextReward
        
    if currentBoard != None and currentAction != None:
        stateActFreq[(currentBoard, currentAction)] += 1
        
        minMax = rewardFunction(nextBoard) if isGameOver(nextBoard) else getMinMaxByBoard(nextBoard, stateActValue, max if turn == O else min)
        stateActValue[(currentBoard, currentAction)] = (stateActValue[(currentBoard, currentAction)] 
                                            + stepSizeFunc(stateActFreq[(currentBoard, currentAction)]) 
                                            * (nextReward + discount * minMax
                                               - stateActValue[(currentBoard, currentAction)]))
        
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

def getBestMove(board, stateActValue, minMax, learning):
    actions = getActions(board)
    actionVals = {}
    result = None
    for act in actions:
        actionVals[stateActValue[(board, act)]] = act
    
    if not learning:
        print actionVals

    if len(actionVals) == 1:
        #all of the actions are equal so choose at random
        result = actions[randint(0, len(actions) - 1)] 
    else:
        #hashed by value of action so return min/max key
        result = actionVals[minMax(actionVals.keys())]
               
    return result

numActions = 0
numRand = 0

def machineTurn(board, stateActValue, machine, learning):
    action = None
    
    global numActions
    numActions += 1
    
    if learning:
        if randint(0, 100) in (0, 1, 2, 3): #should be 4% chance here
            possibles = getActions(board)
            action = possibles[randint(0, len(possibles) - 1)]
            global numRand
            numRand += 1
        else:
            action = getBestMove(board, stateActValue, min if machine == O else max, learning)
    else:
        action = getBestMove(board, stateActValue, min if machine == O else max, learning)
        
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
            
def main():
        playAgain = True
        sameSettings = False
        stateActValue = None
        while playAgain:
            if not sameSettings:
                print "Generating startup data..."
                emptyBoard = generateBoard()
                allPaths = set([])
                allBoards = set([])
                allBoards.add(emptyBoard)
                getAllBoardsAndPaths(emptyBoard, X, allBoards, [emptyBoard], allPaths)
                stateActValue = getStateAction(allBoards)
                stateActFreq = getStateAction(allBoards)

                human = raw_input("Do you want to be x or o? ").lower()
                machine = getTurn(human)
                   
                print "I have to play with myself, hold on..."
                generateGames(stateActValue, stateActFreq, getTurn(machine), machine, 1000000)
                
            print "\nPlay!\n"
            playGame(stateActValue, stateActFreq, human, machine, False)
             
            playAgainInput = raw_input("Do you want to play again (y, n)? ").lower()
            playAgain = True if playAgainInput == 'y' else False
            if playAgain:
                sameSettingsInput = raw_input("Would you like to keep the same settings(i.e. play the same agent again?) (y, n)? ").lower()
                sameSettings = True if sameSettingsInput == 'y' else False 
main()
