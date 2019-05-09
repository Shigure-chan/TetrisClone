#Tetris clone
#Kevin Huang




from tetrimino import Tetrimino

ROWS = 22 #20 for the actual well, 2 for the buffer zone
COLUMNS = 10 #default width


class GameState:
    def __init__(self):
        self.board = [[' * ' for i in range(COLUMNS)] for j in range(ROWS)]


    def board_config(self, columns, rows):
        #board_config(15, 10)

        #Assertion errors are raised so somebody doesn't try to make a board with negative rows and columns...
        assert type(columns) == int and rows >= 4, ('GameState.board_config: columns({}) is not a int that is at least 4'.format(columns))
        assert type(rows) == int and columns >= 4, ('GameState.board_config: rows({}) is not a int that is at least 4'.format(rows))
        
        self.gameboard = [['   ' for i in range(columns)] for j in range(rows)]
    
    def printout(self):
        '''
        creates a string representation of the board
        '''
        return   '\n'.join([ ''.join([self.board[i][j] for j in range(len(self.board[i]))]) for i in range(len(self.board)) ])

    def spawn(self):

        #initializes Tetrimino object
        block = Tetrimino()
        block.spawn()

        #replaces stars with letters symbolizing block type
        for x,y in [block.block1, block.block2, block.block3, block.block4]:
            self.board[x][y] = ' {} '.format(block.block_type)

        


a = GameState()
a.spawn()
print(a.printout())

    
            
