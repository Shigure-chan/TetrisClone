#Kevin Huang

from random import choice

class Tetrimino():
    def __init__(self):
        '''
        Cyan - I 
        Yellow - O 
        Purple - T 
        Green - S 
        Red - Z 
        Blue - J 
        Orange  - L

        The I and O spawn in the middle columns 
        The rest spawn in the left-middle columns 
        The tetriminoes spawn horizontally with J, L and T spawning flat-side first. 
        Spawn above playfield, row 21 for I, and 21/22 for all other tetriminoes.


        rotation_state...
        0 - starting spawn state (the orientation when it first spawns)
        R - one rotation clockwise from 0
        2 - two rotations from 0
        L - one rotation counterclockwise from 0

        0 rotations land you at 0...
        1 rotation CW  lands you at R...
        1 rotation CCW lands you at R......
        [perhaps use indexing...]

        '''
        
        self.block_type = choice(['I', 'O', 'T', 'S', 'Z', 'J', 'L'])
        self.orientation = '0'
        self.rotation_phases = ['0', 'R', '2', 'L']


        
        
        self.blocks = {'block1' : [0,0], 'block2' : [0,0], 'block3' : [0,0], 'block4' : [0,0]}

        self.landed = False
        self.frozen = False

    def set_type(self, type_str):
        '''
        for testing purposes...
        allows one to change the type of a block, handy for unittesting
        '''
        assert type_str in ['I', 'O', 'T', 'S', 'Z', 'J', 'L'], f'Tetrimino.set_type: type_str(\'{type_str}\') must be either \'I\', \'O\', \'T\', \'S\', \'Z\', \'J\', \'L\''
        self.blocktype = type_str
    
    def rotate(self, orientation):
        '''
        allows you to go between different states of rotation
        '''
        assert orientation in ['0', 'R', '2', 'L'], f'Tetrimino.rotate: orientation(\'{orientation}\') must be either \'0\', \'R\', \'2\', \'L\''
        self.rotation = orientation

    def position_blocks(self, row, col):
        '''
        since the blocks use block1 as a reference... this should allow one to circumvent the usual generation

        might have to refactor the individual methods below...
        '''
        assert type(row) == int and type(col) == int
        assert row > 0 and col > 0
        self.blocks['block1'] = [row, col]

    def fall_down(self):
        '''
        adds 1 to the rows index
        '''
        rows = 0
        for i in self.blocks:
            self.blocks[i][rows] += 1
    
    def move_left(self):
        '''
        subtracts 1 from the rows index
        '''
        cols = 1
        for i in self.blocks:
            self.blocks[i][cols] -= 1

    def move_right(self):
        '''
        adds 1 to the rows index
        '''
        cols = 1
        for i in self.blocks:
                self.blocks[i][cols] += 1

    def indexes_below(self) -> [[int, int]]:
        '''
        generates indexes for spaces below the block
        '''
        return [ [i[0]+1, i[1]] for i in [self.blocks[i] for i in sorted(self.blocks)]\
                          if [i[0]+1, i[1]] not in [self.blocks[i] for i in sorted(self.blocks)] ]
        

    def indexes_right(self) -> [[int, int]]:
        '''
        generates indexes for spaces to the right of the block
        '''
        return [ [i[0], i[1]+1] for i in [self.blocks[i] for i in sorted(self.blocks)]\
                if [i[0], i[1]+1] not in [self.blocks[i] for i in sorted(self.blocks)] ]

    def indexes_left(self) -> [[int, int]]:
        return [ [i[0], i[1]-1] for i in [self.blocks[i] for i in sorted(self.blocks)]\
                if [i[0], i[1]-1] not in [self.blocks[i] for i in sorted(self.blocks)] ]


    

        
    def o_block(self):
        '''
        block1 is the upper left block in a "O" piece

        [1][2]
        [3][4]

        
        '''
        
        #block1 generates in the 0th row (1st row, in buffer zone)
        #block1 enerates in columns 0 to 8; otherwise, it could spawn in column 9...
        self.blocks['block1'] = [ 0, choice(range(0,9)) ]
        
        self.blocks['block2'] = [ 0, self.blocks['block1'][1] + 1 ]
        self.blocks['block3'] = [ 1, self.blocks['block1'][1]     ]
        self.blocks['block4'] = [ 1, self.blocks['block1'][1] + 1 ]
        
        return None #prevents recursion...
             
    def i_block(self):
        '''
        block1 is the left-most block when horizontal...
        spawns horizontally...

        these charts are for when we implement rotation...
        
        State 0
        [ ][ ][ ][ ]
        [1][2][3][4]
        [ ][ ][ ][ ]
        [ ][ ][ ][ ]

        0 -> L
        4 is pushed up 1 and 2 to the left
        3 is pushed          1 to the left 
        2 is pushed down 1
        1 is pushed down 2 and 1 to the right

        0 -> R
        4 is pushed down 2 and 1 to the left
        3 is pushed down 1
        2 is pushed up 1 and 1 to the right
        1 is pushed up 1 and 2 to the right

        State R
        [ ][ ][1][ ]
        [ ][ ][2][ ]
        [ ][ ][3][ ]
        [ ][ ][4][ ]

        R -> 0
        4 is pushed up 2 and 1 to the right
        3 is pushed up 1
        2 is pushed          1 to the left
        1 is pushed down 1 and 2 to the left

        R -> 2
        4 is pushed up 1 and 2 to the left
        3 is pushed up 1 and 1 to the left
        2 is pushed down 1 
        1 is pushed down 2 and 1 to the right

        State 2
        [ ][ ][ ][ ]
        [ ][ ][ ][ ]
        [4][3][2][1]
        [ ][ ][ ][ ]

        2 -> R
        4 is pushed down 1 and 2 to the right
        3 is pushed            1 to the right
        2 is pushed up 1 
        1 is pushed up 2 and 1 to the left

        2 -> L
        4 is pushed down 1 and 2 to the right
        3 is pushed            1 to the right
        2 is pushed up 1 
        1 is pushed up 2 and 1 to the left

        State L
        [ ][4][ ][ ]
        [ ][3][ ][ ]
        [ ][2][ ][ ]
        [ ][1][ ][ ]

        L -> 2
        4 is pushed down 2 and 1 to the left
        3 is pushed down 1
        2 is pushed right 1
        1 is pushed up 1 and 2 to the right

        L -> 0
        4 is pushed down 1 and 2 to the right
        3 is pushed            1 to the right
        2 is pushed up 1
        1 is pushed up 2 and 1 to the left
        '''

        self.blocks['block1'] = [ 0, choice(range(0,7)) ] #prevents it from spawning offscreen
        
        self.blocks['block2'] = [ 0, self.blocks['block1'][1] + 1 ]
        self.blocks['block3'] = [ 0, self.blocks['block1'][1] + 2 ]
        self.blocks['block4'] = [ 0, self.blocks['block1'][1] + 3 ]

        return None #prevents recursion...

    def t_block(self):
        '''
        block1 is the left-most block when horizontal...
        spawns horizontally...

        this chart is for when we implement rotation...
        State 0
        [ ][1][ ]
        [2][3][4]
        [ ][ ][ ]
 
        State R 
        [ ][2][ ]
        [ ][3][1]
        [ ][4][ ]
        
        State 2
        [ ][ ][ ]
        [4][3][2]
        [ ][1][ ]

        State L
        [ ][4][ ]
        [1][3][ ]
        [ ][2][ ]
        '''
        self.blocks['block1'] = [ 0, choice(range(1,9)) ] #prevents it from spawning offscreen

        self.blocks['block2'] = [ 1, self.blocks['block1'][1] - 1 ]
        self.blocks['block3'] = [ 1, self.blocks['block1'][1]     ] #center
        self.blocks['block4'] = [ 1, self.blocks['block1'][1] + 1 ]

        return None #prevents recursion...

    def l_block(self):
        '''
        block1 is the right-most when spawned...
        spawns horizontally...
        [ ][ ][1]
        [4][3][2]
        [ ][ ][ ]
        
        '''
        self.blocks['block1'] = [ 0, choice(range(2, 10))]

        self.blocks['block2'] = [ 1, self.blocks['block1'][1]      ]
        self.blocks['block3'] = [ 1, self.blocks['block1'][1] - 1  ] #center
        self.blocks['block4'] = [ 1, self.blocks['block1'][1] - 2  ]

        return None #prevents recursion...

    def j_block(self):
        '''
        block1 is the left-most when spawned...
        spawns horizontally...
        [1][ ][ ]
        [2][3][4]
        [ ][ ][ ]
        
        '''
        self.blocks['block1'] = [ 0, choice(range(0, 8))]

        self.blocks['block2'] = [ 1, self.blocks['block1'][1]     ]
        self.blocks['block3'] = [ 1, self.blocks['block1'][1] + 1 ] #center
        self.blocks['block4'] = [ 1, self.blocks['block1'][1] + 2 ]

        return None #prevents recursion...
    
    def s_block(self):
        '''
        block1 is the right-most when spawned...
        spawns horizontally...
        [ ][2][1]
        [4][3][ ]
        [ ][ ][ ]
        
        '''
        self.blocks['block1'] = [ 0, choice(range(2, 10))]

        self.blocks['block2'] = [ 0, self.blocks['block1'][1] - 1  ]
        self.blocks['block3'] = [ 1, self.blocks['block1'][1] - 1  ] #center
        self.blocks['block4'] = [ 1, self.blocks['block1'][1] - 2  ]

        return None #prevents recursion...

    def z_block(self):
        '''
        block1 is the left-most when spawned...
        spawns horizontally...
        [1][2][ ]
        [ ][3][4]
        [ ][ ][ ]
        
        '''
        self.blocks['block1'] = [ 0, choice(range(0, 8))]

        self.blocks['block2'] = [ 0, self.blocks['block1'][1] + 1 ]
        self.blocks['block3'] = [ 1, self.blocks['block1'][1] + 1 ] #center
        self.blocks['block4'] = [ 1, self.blocks['block1'][1] + 2 ]

        return None #prevents recursion...

    def rotate_left(self):
        '''
        '''
        pass
    
    
    def rotate_right(self):
        '''
    
        '''
        if self.block_type in ['J', 'L', 'S', 'T', 'Z']:
            pass
        elif self.block_type == 'I':
            
            pass

    
    
    def spawn(self):
        if self.block_type == 'O':
            self.o_block()

        elif self.block_type == 'I':
            self.i_block()

        elif self.block_type == 'T':
            self.t_block()

        elif self.block_type == 'L':
            self.l_block()

        elif self.block_type == 'J':
            self.j_block()

        elif self.block_type == 'S':
            self.s_block()

        elif self.block_type == 'Z':
            self.z_block()

    
                








                
