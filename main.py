import random
import copy

class Node:
    def __init__(self, board, turn):
        """
        Initializes the node with it's board value, children, current turn, and minimax value
        """
        self.board = board
        self.children = []
        self.turn = turn
        self.value = self.getminimax()
    def getNextTurn(self):
        """
        Gets the next turn based on the turn initialized with the node
        """
        self.nextTurn = ''
        if self.turn == 'x':
            self.nextTurn = 'o'
        elif self.turn == 'o':
            self.nextTurn = 'x'
        return(self.nextTurn)
    def getminimax(self):
        """
        Gets minimax value (1 for win, 0 for draw, -1 for loss)
        """
        terminal = self.terminalPos()
        if terminal[0]:
            if terminal[1] == 'x':
                self.value = 1
            elif terminal[1] == 'o':
                self.value = -1
            else:
                self.value = 0
            return(self.value)
    def makeMove(self,move,turn):
        """
        Makes a move given x or o and a number 1-9
        """
        if move%3 == 0:
            self.board[int(move/3)-1][(move-3*int(move/3))-1] = turn
        else:
            self.board[int(move/3)][(move-3*int(move/3))-1] = turn
        self.value = self.getminimax()
    def display(self):
        """
        Displays board
        """
        for item in self.board:
            print(item[0] + ' ' + item[1] + ' ' + item[2])
    def findLegalMoves(self):
        """
        Returns dictionary of all legal moves
        """
        pos = 1
        legalmoves = []
        for item in self.board:
            for iitem in item:
                if iitem == '-':
                    legalmoves.append(pos)
                pos = pos + 1
        return(legalmoves)
    def terminalPos(self):
        """
        Returns if the board is in a terminal position, and if so,
        if it is a draw, win, or loss
        """
        if self.board[0][0] != "-" and self.board[1][0] == self.board[0][0] and self.board[2][0] == self.board[0][0]:
          return True, self.board[0][0]
        elif self.board[0][1] != "-" and self.board[1][1] == self.board[0][1] and self.board[2][1]== self.board[0][1]:
          return True, self.board[0][1]
        elif self.board[0][2] != "-" and self.board[1][2] == self.board[0][2] and self.board[2][2]== self.board[0][2]:
          return True, self.board[0][2]
        elif self.board[0][0] != "-" and self.board[0][1] == self.board[0][0] and self.board[0][2]== self.board[0][0]:
          return True, self.board[0][0]
        elif self.board[1][0] != "-" and self.board[1][1] == self.board[1][0] and self.board[1][2]== self.board[1][0]:
          return True, self.board[1][0]
        elif self.board[2][0] != "-" and self.board[2][1] == self.board[2][0] and self.board[2][2]== self.board[2][0]:
          return True, self.board[2][0]
        elif self.board[0][0] != "-" and self.board[1][1] == self.board[0][0] and self.board[2][2]== self.board[0][0]:
          return True, self.board[0][0]
        elif self.board[0][2] != "-" and self.board[1][1] == self.board[0][2] and self.board[2][0]== self.board[0][2]:
          return True, self.board[0][2]

        for i in self.board:
          for j in i:
            if j == "-":
              return False, None

        return True, "Draw"
class Tree:
    def __init__(self, root):
        """
        Initializes the tree with the root node
        """
        self.root = root
    def buildChildren(self, node):
        """
        Builds all children of a given node
        """
        legalMoves = node.findLegalMoves()
        for legalMove in legalMoves:
            self.newboard = copy.deepcopy(node)
            self.newboard.children.clear()
            self.newboard.turn = node.getNextTurn()
            self.newboard.makeMove(legalMove, self.turn)
            node.children.append(self.newboard)
    def buildTree(self, node):
        """
        Recursively builds tree of all possible board states
        """
        self.turn = node.turn
        self.buildChildren(node)
        for child in node.children:
            self.winLoss = child.terminalPos()
            if self.winLoss[0]:
                pass
            else:
                self.buildTree(child)
    def minimax(self, move, vals):
        """
        Gets the minimax value of a node given all terminal positions
        that can occur after it's state
        """
        if move.terminalPos()[0]:
            vals.append(move.value)
        for child in move.children:
            self.minimax(child, vals)
        self.minimaxVal = sum(vals) / len(vals)
    def checkEnd(self):
        """
        Checks if the game is over
        """
        if self.currentBoard.terminalPos()[0]:
            self.currentBoard.display()
            if self.currentBoard.terminalPos()[1] == 'x':
                print("You lose!")
            elif self.currentBoard.terminalPos()[1] == 'o':
                print("You win!")
            else:
                print("Draw!")
    def playGame(self):
        """
        Plays the game
        """
        while True:
            self.currentBoard = copy.deepcopy(self.root)
            self.currentTurn = 'x'
            turn = 0
            while True:
                self.currentBoard.display()
                if self.currentTurn == 'x':
                    self.turnVals = {}
                    legalMoves = self.currentBoard.findLegalMoves()
                    if turn == 0:
                        self.currentBoard.makeMove(5,'x') # 5 is the most efficient first move
                        print("Computer plays: 5")
                    else:
                        for child in self.currentBoard.children:
                            self.minimax(child, [])
                            self.turnVals[legalMoves[self.currentBoard.children.index(child)]] = self.minimaxVal
                        self.currentBoard.makeMove(max(self.turnVals, key=self.turnVals.get),'x')
                        print('Computer plays:', str(max(self.turnVals, key=self.turnVals.get)))

                self.checkEnd()
                if self.currentBoard.terminalPos()[0]:
                    break

                if self.currentTurn == 'o':
                    validMove = False
                    while not validMove:
                        self.playerMove = int(input("Move: "))
                        if self.playerMove in self.currentBoard.findLegalMoves():
                            break
                        else:
                            print('invalid move.')
                    self.currentBoard.makeMove(self.playerMove,'o')

                self.checkEnd()
                if self.currentBoard.terminalPos()[0]:
                    break

                if self.currentTurn == 'x':
                    self.currentTurn = 'o'
                else:
                    self.currentTurn = 'x'

                for child in self.currentBoard.children: # Sets the current board equal to one of it's children
                    if child.board == self.currentBoard.board:
                        self.currentBoard = child
                turn = turn + 1
            playAgain = input("Play again? (y/n): ")
            if playAgain == 'y':
                continue
            else:
                print("Thanks for playing!")
                break
                
board = [['-','-','-'],['-','-','-'],['-','-','-']]
node = Node(board, 'x')
tree = Tree(node)
tree.buildTree(node)
tree.playGame()

#0 - 0.244
#1 - 0.137
#2 - 0.244
#3 - 0.137
#4 - 0.388
#5 - 0.137
#6 - 0.244
#7 - 0.137
#8 - 0.244
