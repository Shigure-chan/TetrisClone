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
        '''
        self.block_type = choice(['I', 'O', 'T', 'S', 'Z', 'J', 'L'])

        self.block1 = [0,0]
        self.block2 = [0,0]
        self.block3 = [0,0]
        self.block4 = [0,0]
        
    def o_block(self):
        '''
        block1 is the upper left block in a "O" piece

        [1][2]
        [3][4]
        '''
        
        #block1 generates in the 0th row (1st row, in buffer zone)
        #block1 enerates in columns 0 to 8; otherwise, it could spawn in column 9...
        self.block1 = [ 0, choice(range(0,9)) ]
        
        self.block2 = [ 0, self.block1[1] + 1 ]
        self.block3 = [ 1, self.block1[1]     ]
        self.block4 = [ 1, self.block1[1] + 1 ]
        
        return None #prevents recursion...
             
    def i_block(self):
        '''
        block1 is the left-most block when horizontal...
        spawns horizontally...

        this chart is for when we implement rotation...
        [ ][ ][ ][ ]
        [1][2][3][4]
        [ ][ ][ ][ ]
        [ ][ ][ ][ ]
        '''
        self.block1 = [ 0, choice(range(0,7)) ] #prevents it from spawning offscreen
        
        self.block2 = [ 0, self.block1[1] + 1 ]
        self.block3 = [ 0, self.block1[1] + 2 ]
        self.block4 = [ 0, self.block1[1] + 3 ]

        return None #prevents recursion...

    def t_block(self):
        '''
        block1 is the left-most block when horizontal...
        spawns horizontally...

        this chart is for when we implement rotation...
        [ ][1][ ]
        [2][3][4]
        [ ][ ][ ]
        [ ][ ][ ]
        '''
        self.block1 = [ 0, choice(range(1,9)) ] #prevents it from spawning offscreen

        self.block2 = [ 1, self.block1[1] - 1 ]
        self.block3 = [ 1, self.block1[1]     ]
        self.block4 = [ 1, self.block1[1] + 1 ]

        return None #prevents recursion...

    def l_block(self):
        '''
        block1 is the right-most when spawned...
        spawns horizontally...
        [ ][ ][1]
        [4][3][2]
        [ ][ ][ ]
        [ ][ ][ ]
        '''
        self.block1 = [ 0, choice(range(2, 10))]

        self.block2 = [ 1, self.block1[1]      ]
        self.block3 = [ 1, self.block1[1] - 1  ]
        self.block4 = [ 1, self.block1[1] - 2  ]

        return None #prevents recursion...

    def j_block(self):
        '''
        block1 is the left-most when spawned...
        spawns horizontally...
        [1][ ][ ]
        [2][3][4]
        [ ][ ][ ]
        [ ][ ][ ]
        '''
        self.block1 = [ 0, choice(range(0, 8))]

        self.block2 = [ 1, self.block1[1]     ]
        self.block3 = [ 1, self.block1[1] + 1 ]
        self.block4 = [ 1, self.block1[1] + 2 ]

        return None #prevents recursion...
    
    def s_block(self):
        '''
        block1 is the right-most when spawned...
        spawns horizontally...
        [ ][2][1]
        [4][3][ ]
        [ ][ ][ ]
        [ ][ ][ ]
        '''
        self.block1 = [ 0, choice(range(2, 10))]

        self.block2 = [ 0, self.block1[1] - 1  ]
        self.block3 = [ 1, self.block1[1] - 1  ]
        self.block4 = [ 1, self.block1[1] - 2  ]

        return None #prevents recursion...

    def z_block(self):
        '''
        block1 is the left-most when spawned...
        spawns horizontally...
        [1][2][ ]
        [ ][3][4]
        [ ][ ][ ]
        [ ][ ][ ]
        '''
        self.block1 = [ 0, choice(range(0, 8))]

        self.block2 = [ 0, self.block1[1] + 1 ]
        self.block3 = [ 1, self.block1[1] + 1 ]
        self.block4 = [ 1, self.block1[1] + 2 ]

        return None #prevents recursion...
    
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

    
                








                
