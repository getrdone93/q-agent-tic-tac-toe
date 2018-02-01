#!/usr/bin/python
from random import randint
from common import *
import pickle

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