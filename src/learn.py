#!/usr/bin/python
from common import *

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

def generateGames(stateActValue, stateActFreq, machine1, machine2, numTimes):
    games = []
    for i in range(0, numTimes):
        if i % 10000 == 0:
            print "I'm %f percent done playing with myself" % ((float(i) / numTimes) * 100)
        playGame(stateActValue, stateActFreq, machine1, machine2, True)
    return games

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


emptyBoard = generateBoard()
allBoards = set([])
allBoards.add(emptyBoard)
getAllBoards(emptyBoard, X, allBoards)
stateActValue = getStateAction(allBoards)
stateActFreq = getStateAction(allBoards)
          