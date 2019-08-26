#Tetris clone
#Kevin Huang




from tetrimino import Tetrimino
from random import shuffle

ROWS = 22 #20 for the actual well, first 2 for the buffer zone
COLUMNS = 10 #default width
CLEAR_STRING = ' # '


class GameState:
    ROWS = 22
    COLUMNS = 10

    def __init__(self):
        self.board = [[' * ' for i in range(self.COLUMNS)] for j in range(self.ROWS)]
        self.block = None
        self.existing_blocks = [] #a list of tetromino objects

        self.block_types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
        shuffle(self.block_types)
        self.queue = self.block_types[:]

        self.hold_queue = [] #this should be empty most of the time...

        

    def block_pieces(self) -> {str:[int, int]}:
        '''
        returns a dict of the coordinates for easy access
        '''
        assert type(self.block) == Tetrimino, 'GameState.block_pieces: self.block is not a Tetrimino object'
        return self.block.blocks

    def existing_blocks_list(self) -> [str]:
        return [str(i) for i in self.existing_blocks]

    def block_coords_deleter(self, specific_block: [int, int]):
        for tetrimino in self.existing_blocks:
            blocks_to_delete = []
            for block in tetrimino.blocks:
                if tetrimino.blocks[block] == specific_block:
                    blocks_to_delete.append(block)
            for i in blocks_to_delete:
                del tetrimino.blocks[i]
    
    def block_deleter(self):
        '''
        makes sure that if a block doesn't exist (no more coordinates), it just deletes the block object completely from the game
        '''
        self.existing_blocks = [block for block in self.existing_blocks if len(block.blocks) != 0]
        
    def printout(self) -> str:
        '''
        creates a string representation of the board

        keep in mind that this still shows the buffer zone... 
        
        '''
        return   '\n'.join([ ''.join([self.board[i][j] for j in range(len(self.board[i]))]) for i in range(len(self.board)) ])
    
    def ghost_printout(self):
        field = [[self.board[i][j] for j in range(len(self.board[i]))] for i in range(len(self.board)) ]

        print(self.hard_drop_coords())

        for j,k in self.hard_drop_coords().values():
            if [j,k] not in self.block.blocks.values(): #basically we should see the parts of the ghost block that are not currently occupied by the current block
                field[j][k] = '({})'.format(self.block.block_type)

        return '\n'.join([ ''.join([field[i][j] for j in range(len(field[i]))]) for i in range(len(field)) ]) 

    def spawn(self):
        '''
        -initializes a tetrimino
        -sets it to the first type in the queue
        -spawns the block on the board
        -adds the block to the list of existing blocks
        -deletes the first type and appends it to the queue

        '''
        self.block = Tetrimino()

        current_type = self.queue[0]

        self.block.set_type(current_type)
        
        self.block.spawn()
        self.existing_blocks.append(self.block)

        del self.queue[0]
        self.queue.append(current_type)
    
    def hold(self):
        '''
        We check first to see if we have a current block and the hold_queue is empty and that the block we want to hold is not frozen

        If true, we do the rest of this method...
        We add the current block type to the the hold queue and delete the current block from the existing blocks
        
        '''
        print(self.queue)

        if self.block and len(self.hold_queue) == 0 and not self.block.frozen:  
            self.hold_queue.append(self.block.block_type)
        
            for i in range(len(self.existing_blocks[:])):
                if self.block == self.existing_blocks[i]:
                    del self.existing_blocks[i]
        
        elif self.block.block_type not in self.hold_queue and len(self.hold_queue) == 1 and not self.block.frozen:
            #we add the new value to the hold queue
            
            self.hold_queue.append(self.block.block_type) 

            #we make sure the block with the new value is deleted...
            for i in range(len(self.existing_blocks[:])):
                if self.block == self.existing_blocks[i]:
                    del self.existing_blocks[i]
            
            self.queue.remove(self.hold_queue[0]) 
            #we remove the first occurence of the old value held from the queue to put it at the beginning of the queue
             #without creating a duplicate

            self.queue.insert(0, self.hold_queue[0])
            
            del self.hold_queue[0]
    
    
    def clear_hold_queue(self):
        '''
        Automatically clears hold_queue when a block is spawned
        '''
        if self.block.block_type in self.hold_queue:
            del self.hold_queue[0]

    def print_next_block(self) -> str:
        '''
        prints ths first block in the queue
        '''
        return self.queue[0]


    def print_queue(self) -> [str]:
        '''
        prints the six blocks after the very next block
        '''
        return self.queue[1:7]
    
    def print_hold_queue(self) -> list:
        '''
        prints the hold queue
        '''
        return self.hold_queue


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
    
    def hard_drop_coords(self):
        block_coords = self.block.blocks.copy()
        bottom_value = max([i[0] for i in block_coords.values()])

        hard_drop = {block: [21, block_coords[block][1]] for block in block_coords}
        
        for i in range(1, 22 - bottom_value):
            hard_drop = {block: [block_coords[block][0] + i, block_coords[block][1]] for block in block_coords}
            current_pos = {i: [hard_drop[i][0] - 1, hard_drop[i][1] ] for i in hard_drop}


            if any([self.board[x][y] != ' * ' for x,y in hard_drop.values() if [x,y] not in current_pos.values()]):
                return current_pos

        
        return hard_drop
        
        

    
    def hard_drop(self):
        '''
        In Tetris, we need to make blocks immediately fall down...

        To hard drop... we get the current bottom... At most, all four blocks. 
        Then, we use a for loop to test each row and column value below the 'bottom' to see how many we must move down
        Then we check to see if we can use the spaces for the 'top'
        If this doesn't work, we take the next value...
        '''
        block_coords = self.block.blocks.copy()
        bottom_value = max([i[0] for i in block_coords.values()])

        for i in range(1, 22 - bottom_value):
            
            hard_drop = {block: [block_coords[block][0] + i, block_coords[block][1]] for block in block_coords}
            current_pos = {i: [hard_drop[i][0] - 1, hard_drop[i][1] ] for i in hard_drop}

            if any([self.board[x][y] != ' * ' for x,y in hard_drop.values() if [x,y] not in current_pos.values()]):
                self.block.landed = True
                self.block.frozen = True
                self.block.blocks = current_pos
                break
        else:
            self.block.landed = True
            self.block.frozen = True
            self.block.blocks = hard_drop

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


    def mark_lines(self):
        '''
        REQUIRES TESTING!!!!!!
        replaces any rows full of only letters (nested lists) stored in self.board with rows of clear_strings

        -I'm assuming all I have to do is check if a row or a list is full
        -Then, I show the matching.
        -Then, I empty the row.
        -Then I push the rows down. Hopefully, I don't do this recursively.
        -I'll do more research on this, but this seems rather straightforward to be honest.
        '''
        indexes = []
        
        for i in range(len(self.board)):
            if ' * ' not in self.board[i]:
                self.board[i] = [CLEAR_STRING for i in range(COLUMNS)]
                indexes.append(i)
            
    

        
      

    def line_clear(self):
        #print('line_clear')
        
        coords = []

        #collects the coordinates
        for row in range(len(self.board)):
            if self.board[row] == [CLEAR_STRING for i in range(COLUMNS)]:
                for column in range(COLUMNS):
                    coords.append([row, column])
        
        #deletes the coordinates from the blocks because the update function relies primarily on existing block coordinates
        for coord in coords:
            self.block_coords_deleter(coord)
        
        #deletes any block objects with no coordinates...
        self.block_deleter()

        
        #the blocks above cleared lines end up getting hard dropped...
            #collect the indexes of the rows cleared
            #compare the row index of any block above that row
            #if four lines are cleared under a block, we add four to the row index of that block
        
        #print(self.existing_blocks_list())
        #print()

        for block in self.existing_blocks:
            for coord in block.blocks:
                block.blocks[coord][0] += len({i[0] for i in coords if i[0] > block.blocks[coord][0]}) #rows 19 and 20 are cleared; thus 18 goes down two rows, 
        
        
        
        #print(self.existing_blocks_list())
        
    
    def lock_out(self):
        '''
        triggers when a whole tetrimino locks down above the sky line

        the sky line i assume is the first two rows... so rows 1,2 or indexes 0,1
        if the block is frozen and all coordinates are inside.. trigger gameover
        '''
        
        if self.block.frozen and all([i[0] in [0, 1] for i in self.block.blocks.values()]):
            print("LOCK OUT")
            print("GAME OVER")
            print("end rewards...")
            print("high score table...")

            raise Exception

    def block_out(self):
        '''
        triggers when part of a newly-generated tetrimino is blocked due to an existing block in the matrix

        first, we check that a newly generated tetrimino will not be blocked,
            the new block's coordinates will be checked

            if any of those coordinates are occupied already, end game
                otherwise handle the block like normal
        '''
        block_coords = self.block.blocks.values()

        for j,k in block_coords:
            if self.board[j][k] != ' * ':
                print("BLOCK OUT")
                print("GAME OVER")
                print("end rewards...")
                print("high score table...")
        
                raise Exception

                
                    


            
            


if __name__ == '__main__':

    #Testing methods in console version
    a = GameState()
    counter = 1
    print('State {}'.format(counter))
    print()
    
    while True:
        counter += 1
        print('State {}'.format(counter))
        print('Next: {}'.format(a.print_next_block()))
        print('Queue: {}'.format(a.print_queue()))
        print('Hold: {}'.format(a.print_hold_queue()))
        

        try:
            test = input()
            assert type(test) == str, 'input must be a str type object'
        except AssertionError:
            print('Continuing test')
        else:
            
            if test == '>':
                a.move_right()
                a.board_update()
                print(a.hard_drop_coords()) #test ghost block
                #print(a.printout())
                print(a.ghost_printout())
                print()
                
            elif test == '<':
                a.move_left()
                a.board_update()
                print(a.hard_drop_coords()) #test ghost block
                #print(a.printout())
                print(a.ghost_printout())
                print()
                
            elif test.lower() == 'q':
                break
            
            elif test.lower() == 's':
                a.spawn()
                a.block_out() #tests game over possibility

                a.board_update()
                #print(a.printout())
                print(a.ghost_printout())
                #a.clear_hold_queue()
                print()
            
            elif test.lower() == 'ss':
                while True:
                    b = input('Block Type: ')
                    if b.upper() in ['I', 'O', 'T', 'S', 'Z', 'J', 'L']:
                        break

                a.test_spawn(b.upper())
                a.board_update()
                print(a.printout())
                print()
            
            elif test.lower() == 'l':
                print(a.block.blocks) #before rotation
                a.rotation(value=-1) #revamped rotation method--this is the one that will implement wall kicking
                a.board_update() 
                print(a.hard_drop_coords()) #test ghost block
                #print(a.printout())
                print(a.ghost_printout())
                print()

            elif test.lower() == 'r':
                print(a.block.blocks) #before rotation
                a.rotation(value=1) #revamped rotation method--this is the one that will implement wall kicking
                a.board_update()
                print(a.hard_drop_coords()) #test ghost block
                #print(a.printout())
                print(a.ghost_printout())
                print()

            elif test == '':
                
                a.gravity() #blocks fall, land, freeze
                a.board_update() #board does any updates
                a.mark_lines()
                #print(a.hard_drop_coords()) #test ghost block
                #print(a.printout())
                print(a.ghost_printout())
                a.line_clear()

                a.lock_out() #tests possible gameover
                print()

            elif test == '^':
                a.hard_drop()
                a.board_update()
                print(a.printout())
                print()

            elif test == 'h':
                a.hold()
                a.board_update()
                print(a.printout())
                print()

            elif test == 'p':
                print(a.board)
                print()

        

        
    



    
            
