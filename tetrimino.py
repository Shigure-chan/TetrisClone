from random import choice

class Tetrimino():
    def __init__(self):
        self.block_type = choice(['I', 'O', 'T', 'S', 'Z', 'J', 'L'])
        #when an Tetrimino object spawns, we want to initialize it with a specific type...
        
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
        
    def field_spawn(self):
        self.block1 = [0,0]
        self.block2 = [0,0]
        self.block3 = [0,0]
        self.block4 = [0,0]
        blocks = [self.block1, self.block2, self.block3, self.block4]
        
        def i_block():
            pass
        def o_block():
            pass
        def t_block():
            pass
        def s_block():
            pass
        def z_block():
            pass
        def j_block():
            pass
        def l_block():
            pass
        pass
        


