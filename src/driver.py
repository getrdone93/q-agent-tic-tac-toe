#!/usr/bin/python
#from __builtin__ import enumerate

BOARD_LEN = 9
X = 'x'
O = 'o'

class State():
    def __init__(self, board = None, value = None):
        self.board = board
        self.value = value
#     def __str__(self):
#         result = "board: " + ''.join(map(str, self.board)) + "\n" + "\tvalue: " + ValueError
#         return result
    
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

def enumerateBoards(board, turn, allBoards):
    boardActions = getActions(board)
    while boardActions != []:
        root = invokeAction(boardActions.pop(), turn, board)
        allBoards.add(root)
        if isGameOver(root):
            #board represents a finished game so other player can't go
            #thus no recursive call needs to be made
            continue
        enumerateBoards(root, getTurn(turn), allBoards)
 
def getNonTerminalBoards(allBoards):
    return [board for board in allBoards if not isGameOver(board)] 
        
def getStateAction(nonTermBoards):
    result = {}
    for board in nonTermBoards:
        actions = getActions(board)
        for act in actions:
            result[tuple([board, act])] = 0
    return result
     
emptyBoard = generateBoard()
allBoards = set([])
allBoards.add(emptyBoard)
enumerateBoards(emptyBoard, X, allBoards)
nonTerm = getNonTerminalBoards(allBoards)  
stateActionPairs = getStateAction(nonTerm)

        