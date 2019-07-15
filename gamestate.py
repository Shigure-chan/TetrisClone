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
        assert type(columns) == int and columns >= 4, ('GameState.board_config: columns({}) is not a int that is at least 4'.format(columns))
        assert type(rows) == int and rows >= 4, ('GameState.board_config: rows({}) is not a int that is at least 4'.format(rows))
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
        #initializes random Tetrimino object
        self.block = Tetrimino()
        self.existing_blocks.append(self.block)
        self.block.spawn()

    def test_spawn(self, type_str):
        #initializes custom Tetrimino object
        self.block = Tetrimino()
        self.block.set_type(type_str)
        self.block.spawn()
        self.existing_blocks.append(self.block)
    
        
       

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

    def rotation(self, value=0) -> {str: [int, int]}:
        '''
        1. We find the current orientation and coordinates
        2. We rotate the block
        2. We get the ideal new orientation and coordinates
        3. We rotate the block back
        4. We check the new coordinates depending on which type of block it is...
        5. 
        '''
        current_phase = self.block.orientation() #we need to keep track of the current phase and original coords
        current_coords = self.block.blocks.copy()

        self.block.rotate(value)

        new_phase = self.block.orientation()  #we need to keep track of the new value
        rotation_coords = self.block.blocks.copy() 

        self.block.rotate(-value) 

        print('Current Phase\n',current_phase)
        print('Current coordinates\n', current_coords, '\n')

        print('New Phase\n', new_phase)
        print('Rotation coordinates\n', rotation_coords, '\n')
        
        #each list in the board is each row (first index)
        #each element in the list is each column (second index)

        '''
        [X, X, A, X]
        [X, A, A, X]
        [X, X, A, X]
        '''
    
        def valid_rotation(rotation_coords: dict) -> bool:
            '''
            The valid rotation checks whether the coordinates that a block will rotate into are valid...

            1. First, it filters coordinates to check only the "new" spots; basically to prevent from checking itself...
            2. We check to see if the coordinates are even inside the bounds of the board
            3. We then check if the new spot is "unoccupied"
            '''
            filtered_rotation_coords = [i for i in rotation_coords.values() if i not in current_coords.values()]

            print(filtered_rotation_coords)
            
            for i in filtered_rotation_coords: 
                row= i[0]
                column = i[1]
                
                if row not in range(ROWS): 
                    return False
                if column not in range(COLUMNS):
                    return False
                
                if self.board[row][column] != ' * ':
                    return False
            else:
                return True


        def final_coords_generator(rotation_coords: dict, y_value: int, x_value: int) -> {str: [int, int]}:
            return {i: [rotation_coords[i][0] + y_value, rotation_coords[i][1] + x_value] for i in rotation_coords}

        if valid_rotation(rotation_coords): #Check 1
            self.block.index_changer(value)
            self.block.blocks = rotation_coords #the problem here is that the phase isn't changing...

        elif self.block.block_type in ['J', 'L', 'S', 'T', 'Z']:

            if (current_phase, new_phase) in [('R', '0'), ('R', '2')]:
                if valid_rotation( final_coords_generator(rotation_coords, 0, 1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 0, 1)
            
                elif valid_rotation( final_coords_generator(rotation_coords, -1, 1)  ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, -1, 1) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, 2, 0) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 2, 0)
                
                elif valid_rotation( final_coords_generator(rotation_coords, 2, 1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 2, 1)


            elif (current_phase, new_phase) in [('0', 'R'), ('2', 'R')]:
                if valid_rotation( final_coords_generator(rotation_coords, 0, -1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 0, -1) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, 1, -1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 1, -1) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, -2, 0) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, -2, 0) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, -2, -1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, -2, -1) 


            elif (current_phase, new_phase) in [('2', 'L'), ('0', 'L')]:
                if valid_rotation( final_coords_generator(rotation_coords, 0, 1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 0, 1) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, 1, 1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 1, 1) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, -2, 0) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, -2, 0) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, -2, 1) ):
                    self.block.blocks = final_coords_generator(rotation_coords, -2, 1) 


            elif (current_phase, new_phase) in [('L', '2'), ('L', '0')]:
                if valid_rotation( final_coords_generator(rotation_coords, 0, -1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 0, -1) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, -1, -1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, -1, -1) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, 2, 0) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 2, 0) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, 2, -1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 2, -1) 
            

        elif self.block.block_type == 'I':
            if (current_phase, new_phase) in [('R', '0'), ('2', 'L')]:
                if valid_rotation( final_coords_generator(rotation_coords, 0, 2) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 0, 2)
                
                elif valid_rotation( final_coords_generator(rotation_coords, 0, -1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 0, -1) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, 1, 2) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 1, 2) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, -2, -1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, -2, -1) 


            elif (current_phase, new_phase) in [('0', 'R'), ('L', '2')]:
                if valid_rotation( final_coords_generator(rotation_coords, 0, -2) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 0, -2) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, 0, 1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 0, 1) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, -1, -2) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, -1, -2) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, 2, 1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 2, 1) 


            elif (current_phase, new_phase) in [('R', '2'), ('0', 'L')]:
                if valid_rotation( final_coords_generator(rotation_coords, 0, -1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 0, -1) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, 0, 2) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 0, 2) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, 2, -1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 2, -1) 
        
                elif valid_rotation( final_coords_generator(rotation_coords, -1, 2) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, -1, 2) 


            elif (current_phase, new_phase) in [('2', 'R'), ('L', '0')]:
                if valid_rotation( final_coords_generator(rotation_coords, 0, 1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 0, 1) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, 0, -2) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 0, -2) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, -2, 1) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, -2, 1) 
                
                elif valid_rotation( final_coords_generator(rotation_coords, 1, -2) ):
                    self.block.index_changer(value)
                    self.block.blocks = final_coords_generator(rotation_coords, 1, -2) 


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
            
            elif test.lower() == 'ss':
                while True:
                    b = input('Block Type: ')
                    if b.upper() in ['I', 'O', 'T', 'S', 'Z', 'J', 'L']:
                        break

                a.test_spawn(b)
                a.board_update()
                print(a.printout())
                print()
            
            elif test.lower() == 'l':
                print(a.block.blocks) #before rotation
                a.rotation(value=-1) #revamped rotation method--this is the one that will implement wall kicking
                a.board_update() 
                print(a.printout())
                print()

            elif test.lower() == 'r':
                print(a.block.blocks) #before rotation
                a.rotation(value=1) #revamped rotation method--this is the one that will implement wall kicking
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

                
        

        
    



    
            
