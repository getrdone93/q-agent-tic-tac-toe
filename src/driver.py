#!/usr/bin/python

BOARD_LEN = 9
X = 'x'
O = 'o'

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
        
def getStateAction(nonTermBoards):
    result = {}
    for board in nonTermBoards:
        actions = getActions(board)
        for act in actions:
            result[tuple([board, act])] = 0
    return result

def stepSizeFunc(n):
    return 60 / float((59 + (1 if n == 0 else n)))

def getMaxByBoard(board, dictionary):
    return max([dictionary[key] for key in dictionary if key[0] == board])         
 
def rewardFunction(board):
    if isWin(board, X) or isWin(board, O):
        return 2
    elif isCat(board):
        return 1
    else:
        return -1
 
# def learn(allPaths, stateActValue, stateActFreq, discount):
#     prevBoard = prevAction = prevReward = None
#     for path in allPaths:
#         #q learning agent
#         pathList = list(path)
#         termBoard = pathList.pop(len(pathList) - 1)
#         while pathList != []:
#             board = pathList.pop(0)
#             if prevBoard != None:
#                 stateActFreq[(prevBoard, prevAction)] += 1
#                 stateActValue[(prevBoard, prevAction)] = (stateActValue[(prevBoard, prevAction)] 
#                                                           + stepSizeFunc(stateActFreq[(prevBoard, prevAction)]) 
#                                                           * (prevReward + discount * getMaxByBoard(board, stateActValue) 
#                                                               - stateActValue[(prevBoard, prevAction)]))
            
                
                


# emptyBoard = generateBoard()
# allPaths = set([])
# allBoards = set([])
# getAllBoardsAndPaths(emptyBoard, X, allBoards, [[]], allPaths)
# nonTermBoards = getNonTerminalBoards(allBoards)
# dictionary = getStateAction(nonTermBoards)
# 
# valueNums = [dictionary[key] for key in dictionary if key[0] == list(allBoards)[50]]
# 
# print valueNums

         
        