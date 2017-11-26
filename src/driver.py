#!/usr/bin/python

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

def learn(allPaths, stateActValue, stateActFreq, discount, agentPlayer):
    count = 0
    for path in allPaths:
        count += 1
        if count % 50000 == 0:
            print "On path: " + str(count)
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
            


#print isGameOver(('x', 'o', 'x', 'o', None, 'x', 'o', None, 'x'))
 

emptyBoard = generateBoard()
allPaths = set([])
allBoards = set([])
getAllBoardsAndPaths(emptyBoard, X, allBoards, [[]], allPaths)
    
#print len(allBoards)
#print len(allPaths)
    
stateActValue = getStateAction(allBoards)
stateActFreq = getStateAction(allBoards)

print "got all boards, paths, maps, and hats attempting to learn dough bro"

learn(allPaths, stateActValue, stateActFreq, 1, X)

for val in stateActValue:
    if stateActValue[val] < 0 and not isGameOver(val[0]):
        print "key: " + str(val) + "\tval: " + str(stateActValue[val])
        
# for val in stateActFreq:
#     print "key: " + str(val) + "\tval: " + str(stateActFreq[val])        