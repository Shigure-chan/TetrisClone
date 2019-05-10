#Tetris clone
#Kevin Huang




from tetrimino import Tetrimino

ROWS = 22 #20 for the actual well, 2 for the buffer zone
COLUMNS = 10 #default width


class GameState:
    def __init__(self):
        self.board = [[' * ' for i in range(COLUMNS)] for j in range(ROWS)]
        self.block = None


    def board_config(self, columns, rows):
        #board_config(15, 10)

        #Assertion errors are raised so somebody doesn't try to make a board with negative rows and columns...
        assert type(columns) == int and rows >= 4, ('GameState.board_config: columns({}) is not a int that is at least 4'.format(columns))
        assert type(rows) == int and columns >= 4, ('GameState.board_config: rows({}) is not a int that is at least 4'.format(rows))
        
        self.gameboard = [['   ' for i in range(columns)] for j in range(rows)]
    
    def printout(self):
        '''
        creates a string representation of the board

        keep in mind that this still shows the buffer zone
        
        '''
        return   '\n'.join([ ''.join([self.board[i][j] for j in range(len(self.board[i]))]) for i in range(len(self.board)) ])

    def spawn(self):

        #initializes Tetrimino object
        self.block = Tetrimino()
        self.block.spawn()

        '''
        #replaces stars with letters symbolizing block type
        for x,y in [self.block.block1, self.block.block2, self.block.block3, self.block.block4]:
            self.board[x][y] = ' {} '.format(self.block.block_type)
        '''

    def board_update(self):
        '''
        when a tetrinimo objecct is active and another one spawns, the first one disappears...
        '''
        for i in range(ROWS):
            for j in range(COLUMNS):
                if [i, j] in [self.block.block1, self.block.block2, self.block.block3, self.block.block4]:
                    self.board[i][j] = ' {} '.format(self.block.block_type)
                else:
                    self.board[i][j] = ' * '

    def move_right(self):
        '''
        Checks whether all blocks can be moved to the right

        possible is a bool that determines whether the move stays within the board...

        Eventually, we're going to have to figure out how this can work when blocks are in the squares you attempt to move to...
        Perhaps we can mark them as a gray block.

        '''
        possible = all(map(lambda x:  0 <= x[1] < 9, [self.block.block1, self.block.block2, self.block.block3, self.block.block4]))
        
        if possible:
            self.block.block1[1] += 1
            self.block.block2[1] += 1
            self.block.block3[1] += 1
            self.block.block4[1] += 1

    def move_left(self):
        '''
        Checks whether all blocks can be moved to the left

        possible is a bool that determines whether the move stays within the board...

        Eventually, we're going to have to figure out how this can work when blocks are in the squares you attempt to move to...
        Perhaps we can mark them as a gray block.

        '''
        possible = all(map(lambda x:  0 < x[1] <= 9, [self.block.block1, self.block.block2, self.block.block3, self.block.block4]))

        if possible:
            self.block.block1[1] -= 1
            self.block.block2[1] -= 1
            self.block.block3[1] -= 1
            self.block.block4[1] -= 1

    def gravity(self):
        '''
        Moves blocks down each tick
        possible is a bool that determines whether the move stays within the board...

        We will eventually need to check what will happen if a block is right below another...
        '''

        possible = any(map(lambda x: 1 <= x[0]+1 < 21, [self.block.block1, self.block.block2, self.block.block3, self.block.block4]))

        if possible:
            self.block.block1[0] += 1
            self.block.block2[0] += 1
            self.block.block3[0] += 1
            self.block.block4[0] += 1


if __name__ == '__main__':

    #Testing methods in console version
    a = GameState()
    counter = 1
    print('State {}'.format(counter))
    print(a.printout())
    print()
    
    while True:
        counter += 1
        print('State {}'.format(counter))
        try:
            test = input()
            assert type(test) == str, 'input must be a str type object'
        except AssertionError:
            print('Continuing test')
        else:
            if test == '>':
                a.move_right()
                a.board_update()
                print(a.printout())
                print()
                
            elif test == '<':
                a.move_left()
                a.board_update()
                print(a.printout())
                print()
                
            elif test.lower() == 'q':
                break
            
            elif test.lower() == 's':
                a.spawn()
                a.board_update()
                print(a.printout())
                print()
                
            elif test == '':
                a.gravity()
                a.board_update()
                print(a.printout())
                print()
                
        

        
    



    
            
