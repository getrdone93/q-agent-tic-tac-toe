#!/usr/bin/python
from src.common import getActions, invokeAction, generateBoard, X, machineTurn, \
    getAction, isGameOver, isWin, isCat, getTurn, loadStateActValueFile


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

def playGame(stateActValue, human, machine):
    board = generateBoard()
    turn = human if human == X else machine 
    print "Initial board: "
    gameOver = False;
    while not gameOver:
        printBoard(board)
        if turn == human:
            newBoard = humanTurn(board, human)
        else:
            newBoard = machineTurn(board, stateActValue, machine, False)
            print "Machine move: " + str(getAction(board, newBoard))
                
        board = newBoard
        gameOver = isGameOver(board)
        if gameOver:
            if isWin(board, human):
                print "Human wins!"
            elif isWin(board, machine):
                print "Machine wins!"
            elif isCat(board):
                print "Draw!"
            printBoard(board)
        else:
            turn = getTurn(turn)

def main():
        playAgain = True
        stateActValue = loadStateActValueFile()
        while playAgain:
            human = raw_input("Do you want to be x or o? ").lower()
            machine = getTurn(human)
            print "\nPlay!\n"
            playGame(stateActValue, human, machine)
            playAgainInput = raw_input("Do you want to play again (y, n)? ").lower()
            playAgain = True if playAgainInput == 'y' else False
main()