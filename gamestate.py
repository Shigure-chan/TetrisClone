#Tetris clone
#Kevin Huang




from tetrimino import Tetrinimo

ROWS = 24 #20 for the actual well, 4 for the buffer zone
COLUMNS = 10 #default width


class GameState:
    def __init__(self):
        self.board = [['   ' for i in range(COLUMNS)] for j in range(ROWS)]


    def board_config(self, columns, rows):
        #board_config(15, 10)

        #Assertion errors are raised so somebody doesn't try to make a board with negative rows and columns...
        assert type(columns) == int and rows >= 4, ('GameState.board_config: columns({}) is not a int that is at least 4'.format(columns))
        assert type(rows) == int and columns >= 4, ('GameState.board_config: rows({}) is not a int that is at least 4'.format(rows))
        
        self.gameboard = [['   ' for i in range(columns)] for j in range(rows)]
    
    def printout(self):
        #try to make this so that this returns a string that we can check using a unit test...
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i][j])
            print()

    def spawn(self):
        #this should somehow update the board with a Tetrinimo object and 
        pass

        

a = GameState()
print(a.printout())



    
            
