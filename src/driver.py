#!/usr/bin/python
import random 

BOARD_LEN = 9
X = 'x'
O = 'o'
WIN_REWARD = 2
CAT_REWARD = 0
NON_TERM_REWARD = -.1
LOSS_REWARD = -2
EXPLORE_MAX = 5

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
    #left to right wins
    if ((board[0] == char and board[1] == char and board[2] == char)
    or (board[3] == char and board[4] == char and board[5] == char)
    or (board[6] == char and board[2] == char and board[8] == char)
    #top to bottom wins
    or  (board[0] == char and board[3] == char and board[6] == char)
    or  (board[1] == char and board[4] == char and board[7] == char)
    or  (board[2] == char and board[5] == char and board[8] == char)
    #diagonal wins
    or  (board[0] == char and board[4] == char and board[8] == char)
    or  (board[2] == char and board[4] == char and board[6] == char)):
        return True
    return False
        
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
        else:
            actions = getActions(board)
            for act in actions:
                result[(board, act)] = 0
    result[((), None)] = 0
    return result

def stepSizeFunc(n):
    return 60 / float((59 + (1 if n == 0 else n)))

def getMaxByBoard(board, dictionary):
    return max([dictionary[key] for key in dictionary if key[0] == board])         

def rewardFunction(board, player):
    if board == ():
        return NON_TERM_REWARD
    elif isWin(board, player):
        return WIN_REWARD
    elif isWin(board, X if player == O else O):
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

def getBestAction(board, stateActFreq, stateActValue):
    actions = getActions(board)
    maxVal = -float("inf")
    result = None
    for act in actions:
        tempVal = explorationFunc(stateActValue[(board, act)], stateActFreq[(board, act)])
        if maxVal < tempVal:
            maxVal = tempVal
            result = act
    return result

def getPaths(allPaths, timeUb):
    #can learn at about 6000 paths / minute or 2% of space
    result = set([])
    if (timeUb == -1):
        return allPaths
    else:
        apList = list(allPaths)
        numBlocks = timeUb * 6000 #block size is 6000
        size = 0
        while size < int(numBlocks):
            result.add(apList[random.randint(0, len(apList) - 1)])
            size += 1
    return result    
            
def learn(allPaths, stateActValue, stateActFreq, discount, agentPlayer):
    count = 0
    for path in allPaths:
        count += 1
        if count % 2000 == 0:
            print "learning...completion percentage: {0:.0%}".format(count / float(len(allPaths)))
        pathList = list(path)
        prevBoard = prevAction = prevReward = None
        while pathList != []:
            #q learning agent
            board = pathList.pop(0)
            if board != () and isGameOver(board):
                stateActValue[(board, None)] = rewardFunction(board, agentPlayer)
            if prevBoard != None:
                stateActFreq[(prevBoard, prevAction)] += 1
                stateActValue[(prevBoard, prevAction)] = (stateActValue[(prevBoard, prevAction)] 
                                                          + stepSizeFunc(stateActFreq[(prevBoard, prevAction)]) 
                                                          * (prevReward + discount * getMaxByBoard(board, stateActValue) 
                                                              - stateActValue[(prevBoard, prevAction)]))
            prevAction = getBestAction(board, stateActFreq, stateActValue)    
            prevBoard = board
            prevReward = rewardFunction(prevBoard, agentPlayer)

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

def getBestMove(board, stateActValue):
    actions = getActions(board)
    maxVal = -float("inf")
    result = None
    for act in actions:
        tempVal = stateActValue[(board, act)]
        if maxVal < tempVal:
            maxVal = tempVal
            result = act
    return result

def machineTurn(board, stateActValue, machine):
    action = getBestMove(board, stateActValue)
    print "Machine move: " + str(action)
    return invokeAction(action, machine, board) 
       
def playGame(stateActValue, human, machine):
    board = generateBoard()
    turn = human if human == X else machine 
    while True:
        printBoard(board)
        if turn == human:
            board = humanTurn(board, human)
        else:
            board = machineTurn(board, stateActValue, machine)
        if isGameOver(board):
            if isWin(board, human):
                print "Human wins!"
            elif isWin(board, machine):
                print "Machine wins!"
            elif isCat(board):
                print "Draw!"
            printBoard(board)
            break
        turn = getTurn(turn)
    
def main():
        playAgain = True
        while playAgain:
            emptyBoard = generateBoard()
            allPaths = set([])
            allBoards = set([])
            allBoards.add(emptyBoard)
            getAllBoardsAndPaths(emptyBoard, X, allBoards, [[]], allPaths)
            stateActValue = getStateAction(allBoards)
            stateActFreq = getStateAction(allBoards)
            
            human = raw_input("Do you want to be x or o? ").lower()
            machine = X if human == 0 else O
            timeToLearn = int(raw_input("Enter how long you would like the agent to learn in minutes (-1 for smartest agent): "))
             
            print "generating paths for %s minute learn time" % (timeToLearn)
            paths = getPaths(allPaths, timeToLearn)
            print "Number of trails to be used in learning: " + str(len(paths))
              
            print "Agent will now learn from trials. This should take roughly %s minute(s)" % (timeToLearn)
            learn(paths, stateActValue, stateActFreq, 1, machine)
            
            print "\nPlay!\n"
            playGame(stateActValue, human, machine)
            
            playAgainInput = raw_input("Do you want to play again (y, n)? ").lower()
            playAgain = True if playAgainInput == 'y' else False

main()     