#!/usr/bin/python
from src.common import *
from src.perm_tester import testAgent, PERM_AGENT_WINS

NUM_GAMES = 2000000
DISCOUNT = 1

def updateStateActValue(currentBoard, nextBoard, nextReward, stateActValue, stateActFreq, discount, turn):
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

def stepSizeFunc(n):
    return 60 / float((59 + (1 if n == 0 else n)))

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

def getAllBoards(board, turn, allBoards):
    boardActions = getActions(board)
    while boardActions != []:
        root = invokeAction(boardActions.pop(), turn, board)
        allBoards.add(root)
        if isGameOver(root):
            continue
        getAllBoards(root, getTurn(turn), allBoards)

def playGame(stateActValue, machine1, machine2):
    board = generateBoard()
    turn = machine1 if machine1 == X else machine2 
    gameOver = False;
    while not gameOver:
        if turn == machine1:
            newBoard = machineTurn(board, machine1)
        else:
            newBoard = machineTurn(board, stateActValue, machine2, True)
        
        #learn from move  
        updateStateActValue(board, newBoard, rewardFunction(newBoard), stateActValue, DISCOUNT, turn)
        
        board = newBoard
        gameOver = isGameOver(board)
        if not gameOver:
            turn = getTurn(turn)


def getStateActValue():
    emptyBoard = generateBoard()
    allBoards = set([])
    allBoards.add(emptyBoard)
    getAllBoards(emptyBoard, X, allBoards)
    stateActValue = getStateAction(allBoards)
    stateActFreq = getStateAction(allBoards)
    machine1 = X
    machine2 = O
    
    for i in range(0, NUM_GAMES):
        if i % 10000 == 0:
            print "I'm %f percent done playing with myself" % ((float(i) / NUM_GAMES) * 100)
        playGame(stateActValue, stateActFreq, machine1, machine2, True) 
        
    return stateActValue

def learn():
    isBeatable = True
    numTrials = 0
    while isBeatable:
        print "Testing agent...on trial %d" % (numTrials)
        stateActValue = getStateActValue()
        testAgent(stateActValue, generateBoard(), X, O, X)
        isBeatable = PERM_AGENT_WINS > 0
        if isBeatable:
            #skip next test because agent lost as X
            continue
        
        testAgent(stateActValue, generateBoard(), O, X, X)
        isBeatable = PERM_AGENT_WINS > 0
             