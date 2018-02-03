#!/usr/bin/python
from src.common import *
from src.perm_tester import testQAgent, resetGlobals
    
NUM_GAMES = 2000000
DISCOUNT = 1

def updateStateActValue(currentBoard, nextBoard, nextReward, stateActValue, discount, turn):
    currentAction = getAction(currentBoard, nextBoard)
    if nextBoard != () and isGameOver(nextBoard):
        stateActValue[(currentBoard, currentAction)] += addToValue(stateActValue[(currentBoard, currentAction)], nextReward);
        
    if currentBoard != None and currentAction != None:
        stateActValue[(currentBoard, currentAction)] += addToFrequency(stateActValue[(currentBoard, currentAction)], 1)

        minMax = rewardFunction(nextBoard) if isGameOver(nextBoard) else getMinMaxByBoard(nextBoard, stateActValue, max if turn == O else min)
        newValue = (stepSizeFunc(stateActValue[(currentBoard, currentAction)][1]) 
            * ((nextReward + discount * minMax) - stateActValue[(currentBoard, currentAction)][0]))
        
        stateActValue[(currentBoard, currentAction)] = addToValue(stateActValue[(currentBoard, currentAction)], newValue)

def stepSizeFunc(n):
    return 60 / float((59 + (1 if n == 0 else n)))

#(value, frequency)
def getStateAction(allBoards):
    result = {}
    for board in allBoards:
#         if isGameOver(board):
#             result[(board, None)] = (0, 0)
#         else:
        actions = getActions(board)
        for act in actions:
            result[(board, act)] = (0, 0)
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
            newBoard = machineTurn(board, stateActValue, machine1, True)
        else:
            newBoard = machineTurn(board, stateActValue, machine2, True)
        
        #learn from move  
        updateStateActValue(board, newBoard, rewardFunction(newBoard), stateActValue, DISCOUNT, turn)
        
        board = newBoard
        gameOver = isGameOver(board)
        if not gameOver:
            turn = getTurn(turn)

def getStateActValue(allBoards):
    stateActValue = getStateAction(allBoards)
    machine1 = X
    machine2 = O
    
    for i in range(0, NUM_GAMES):
        if i % 10000 == 0:
            print "I'm %f percent done playing with myself" % ((float(i) / NUM_GAMES) * 100)
        playGame(stateActValue, machine1, machine2) 
        
    return stateActValue

def learn():
    isBeatable = True
    numTrials = 0
    emptyBoard = generateBoard()
    allBoards = set([])
    allBoards.add(emptyBoard)
    getAllBoards(emptyBoard, X, allBoards)
    resetGlobals() #defensive to make sure we have a clean slate
    while isBeatable:
        numTrials += 1
        print "Testing agent...on trial %d" % (numTrials)
        stateActValue = getStateActValue(allBoards)
        isBeatable = testQAgent(stateActValue, X, O)
        resetGlobals()
        if isBeatable:
            #skip next test because agent lost as X
            continue
        isBeatable = testQAgent(stateActValue, O, X)
        if isBeatable:
            resetGlobals()
            
    writeStateActValueFile(stateActValue)

learn()