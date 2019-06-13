#Tetris clone
#Kevin Huang




from tetrimino import Tetrimino

ROWS = 22 #20 for the actual well, first 2 for the buffer zone
COLUMNS = 10 #default width


class GameState:
    ROWS = 22
    COLUMNS = 10

    def __init__(self):
        self.board = [[' * ' for i in range(self.COLUMNS)] for j in range(self.ROWS)]
        self.block = None
        self.existing_blocks = [] #a list of tetromino objects

    def block_pieces(self) -> {str:[int, int]}:
        '''
        returns a dict of the coordinates for easy access
        '''
        assert type(self.block) == Tetrimino, 'GameState.block_pieces: self.block is not a Tetrimino object'
        return self.block.blocks



    def board_config(self, columns, rows):
        #board_config(15, 10)

        #Assertion errors are raised so somebody doesn't try to make a board with negative rows and columns...
        assert type(columns) == int and rows >= 4, ('GameState.board_config: columns({}) is not a int that is at least 4'.format(columns))
        assert type(rows) == int and columns >= 4, ('GameState.board_config: rows({}) is not a int that is at least 4'.format(rows))
        self.COLUMNS = columns
        self.ROWS = rows
        
        self.board = [[' * ' for i in range(self.COLUMNS)] for j in range(ROWS)]
    
    def printout(self) -> str:
        '''
        creates a string representation of the board

        keep in mind that this still shows the buffer zone... 
        
        '''
        return   '\n'.join([ ''.join([self.board[i][j] for j in range(len(self.board[i]))]) for i in range(len(self.board)) ])

    def spawn(self):

        #initializes Tetrimino object
        self.block = Tetrimino()
        self.existing_blocks.append(self.block)
        self.block.spawn()

       

    def board_update(self):
        '''
        when a tetrinimo object is active and another one spawns, the first one disappears...
        '''
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                    self.board[i][j] = ' * '

        if self.block:
            for i in self.existing_blocks:
                for j, k in i.blocks.values():
                    if i.landed == False and i.frozen == False:
                        self.board[j][k] = '|{}|'.format(i.block_type)
                        
                    elif i.landed == True and i.frozen == False:
                        self.board[j][k] = '[{}]'.format(i.block_type)
                        
                    elif i.landed == True and i.frozen == True:
                        self.board[j][k] = ' {} '.format(i.block_type)

    def move_right(self):
        '''
        Checks whether all blocks can be moved to the right

        possible is a bool that determines whether the move stays within the board...

        Eventually, we're going to have to figure out how this can work when blocks are in the squares you attempt to move to...
        Perhaps we can mark them as a gray block.

        '''
        
        dct = self.block_pieces()

        possible = all(map(lambda x:  0 <= x[1] < 9, [dct[i] for i in sorted(dct)]))
        
        if self.block.frozen == False and self.nothing_right() and possible:
            self.block.move_right()

    def move_left(self):
        '''
        Checks whether all blocks can be moved to the left

        possible is a bool that determines whether the move stays within the board...

        Eventually, we're going to have to figure out how this can work when blocks are in the squares you attempt to move to...
        Perhaps we can mark them as a gray block.

        '''
        dct = self.block_pieces()

        possible = all(map(lambda x:  0 < x[1] <= 9, [dct[i] for i in sorted(dct)]))

        if self.block.frozen == False and self.nothing_left() and possible:
            self.block.move_left()

    def gravity(self):
        '''
        Moves blocks down each tick
        possible is a bool that determines whether the move stays within the board...

        We will eventually need to check what will happen if a block is right below another...
        '''
        dct = self.block_pieces()

        possible = all(map(lambda x: 1 <= x[0]+1 < 21, [dct[i] for i in sorted(dct)]))
        #print([self.block.block1, self.block.block2, self.block.block3, self.block.block4])
        #print(self.nothing_below())
        
        if possible and self.nothing_below():
            self.block.fall_down()

        else:
            if self.block.landed == True:
                self.block.frozen = True
                
            elif self.block.landed == False:
                self.block.landed = True
                
                if self.nothing_below():
                    self.block.fall_down()

    def nothing_below(self) -> bool:
        '''
        determines whether there is a block that is in the way of the current block falling down...

        the nothing_below method will work like this...

        it will take a list of current block coordinates and add 1 to the row values..
        if one of the coordinates in the resultant list is in the list of current block coordinates, those values are deleted...
        this keeps this method flexible, especially for when blocks rotate
        
        o-block
        [ [1,0], [1,1], [2,0], [2,1] ] -> [ [2,0], [2, 1], [3, 0], [3,1] ] -> [ [3,0], [3,1] ]

        if there is, it returns True, else False
        '''

        for x,y in self.block.indexes_below():
            if x != ROWS and self.board[x][y] != ' * ':
                return False
        else:
            return True
        

    def nothing_right(self) -> bool:
        '''
        should work similarily to nothing_below
        '''
        
        for x,y in self.block.indexes_right():
            if y != COLUMNS and self.board[x][y] != ' * ':
                return False
        else:
            return True

    def nothing_left(self) -> bool:
        '''
        should work similarily to nothing_below
        '''
        
        for x,y in self.block.indexes_left():
            if y != COLUMNS and self.board[x][y] != ' * ':
                return False
        else:
            return True

    def line_clear(self):
        '''
        REQUIRES TESTING!!!!!!
        replaces any rows full of only letters (nested lists) stored in self.board with rows of clear_strings
        '''
        
        clear_string = '#*#'

        
        for i in range(len(self.board)):
            if ' * ' not in self.board[i]:
                self.board[i] = [clear_string] * COLUMNS

    
    
        
                    
                

            
            


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

            elif test == 'printout':
                print(a.board)
                print()

                
        

        
    



    
            
