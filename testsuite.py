#test suite module
#primarily for testing the methods and functions making up the standard rotation system

import unittest
import random

#modules

import gamestate
import tetrimino
import helper

class TetrisTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None


        self.game = gamestate.GameState()
        self.empty_board = '\n'.join([' *  *  *  *  *  *  *  *  *  * '] * 22)
        

    def test_board_prints_out_all_stars_upon_new_game(self):
        board_string = self.game.printout()
        self.assertEqual(board_string, self.empty_board)

    def test_board_prints_out_with_block_spawned_in_correct_coordinates(self):
        board_list = self.game.board

        self.game.spawn()
        self.game.board_update()
        
        coords = list(self.blocks.values())
        
        for x,y in coords:
            board_list[x][y] = f'|{self.game.block.block_type}|'
        for i in range(len(board_list)):
            board_list[i] = ''.join(board_list[i])
        

        self.assertEqual( self.game.printout(), '\n'.join(board_list) )

    def test_board_block_drops_one_unit_down(self):
        board_list = self.game.board
        

        self.game.spawn()
        self.game.board_update()

        self.game.gravity()
        self.game.board_update()
        
        coords = [self.blocks.values()]
        
        for x,y in coords:
            board_list[x][y] = f'|{self.game.block.block_type}|'
        for i in range(len(board_list)):
            board_list[i] = ''.join(board_list[i])
        

        self.assertEqual( self.game.printout(), '\n'.join(board_list) )
    
    def test_board_block_drops_five_units_down(self):
        board_list = self.game.board
        

        self.game.spawn()
        self.game.board_update()

        for i in range(5):
            self.game.gravity()
            self.game.board_update()
        
        coords = [self.game.block.block1, self.game.block.block2, self.game.block.block3, self.game.block.block4]
        
        for x,y in coords:
            board_list[x][y] = f'|{self.game.block.block_type}|'
        for i in range(len(board_list)):
            board_list[i] = ''.join(board_list[i])
        

        self.assertEqual( self.game.printout(), '\n'.join(board_list) )
    
    def test_board_block_drops_all_the_way_down_even_past_the_board_limit_and_does_not_cause_an_error(self):
        board_list = self.game.board
        

        self.game.spawn()
        self.game.board_update()

        for i in range(23):
            self.game.gravity()
            self.game.board_update()
        
        coords = [self.game.block.block1, self.game.block.block2, self.game.block.block3, self.game.block.block4]
        
        for x,y in coords:
            board_list[x][y] = f'|{self.game.block.block_type}|'
        for i in range(len(board_list)):
            board_list[i] = ''.join(board_list[i])
        

        self.assertEqual( self.game.printout(), '\n'.join(board_list) )

    def test_general_rotation_algorithm_excluding_o_and_i_blocks(self):
        
        self.game.block = tetrimino.Tetrimino()
        self.game.existing_blocks.append(self.game.block)
        

        self.game.block.t_block()

        print()
        self.game.board_update()
        print(self.game.printout())

        center = self.game.block.block3
        center_x = center[1]
        center_y = center[0]

        coords = [self.game.block.block1, self.game.block.block2, self.game.block.block3, self.game.block.block4]
        print(coords)
        for i in range(len(coords)):
            

            xprime = coords[i][1] - center_x
            yprime = coords[i][0] - center_y

            x_doubleprime = ( 0 * xprime ) + (  -1 * yprime )
            y_doubleprime = ( 1 * xprime ) + (  0 * yprime )

            x_doubleprime += center_x
            y_doubleprime += center_y

        
            coords[i] = [x_doubleprime, y_doubleprime]

        
        self.game.board_update()
        print()
        print(self.game.printout())

    def test_counterclockwise_rotation_algorithm(self):
        self.game.board_config(4, 4)
        self.game.board_update()

        self.game.block = tetrimino.Tetrimino()
        self.game.existing_blocks.append(self.game.block)
        

        self.game.block.block_type = 'I'
        self.game.block.block1 = [ 1, random.choice(range(0,1)) ] #prevents it from spawning offscreen
        
        self.game.block.block2 = [ 1, self.game.block.block1[1] + 1 ]
        self.game.block.block3 = [ 1, self.game.block.block1[1] + 2 ]
        self.game.block.block4 = [ 1, self.game.block.block1[1] + 3 ]

        self.game.board_update()

        for i in [self.game.block.block1, self.game.block.block2, self.game.block.block3, self.game.block.block4]:
            '''
            [0, -1] -> 90 CCW
            [1,  0]
            '''
            x = i[1]
            y = i[0]
            
            i[0] = ( 0 * x ) + ( -1 * y )
            i[1] = ( 1 * x ) + (  0 * y )

        self.game.board_update()
        
        
        self.assertEqual( self.game.printout(),
        ' * |I| *  * \n' +
        ' * |I| *  * \n' +
        ' * |I| *  * \n' +
        ' * |I| *  * ')

    def test_clockwise_rotation_algorithm(self):
        self.game.board_config(4, 4)
        self.game.board_update()

        self.game.block = tetrimino.Tetrimino()
        self.game.existing_blocks.append(self.game.block)
        

        self.game.block.block_type = 'I'
        self.game.block.block1 = [ 1, random.choice(range(0,1)) ] #prevents it from spawning offscreen
        
        self.game.block.block2 = [ 1, self.game.block.block1[1] + 1 ]
        self.game.block.block3 = [ 1, self.game.block.block1[1] + 2 ]
        self.game.block.block4 = [ 1, self.game.block.block1[1] + 3 ]

        self.game.board_update()

        for i in [self.game.block.block1, self.game.block.block2, self.game.block.block3, self.game.block.block4]:
            '''
            [  0,  1] -> 90 CW
            [ -1,  0]
            '''
            x = i[1]
            y = i[0]

            xp = 0
            yp = 0
            
                
            i[0] = (  0 * x ) + (  1 * y ) 
            i[1] = (  -1 * x ) + (   0 * y )

            self.game.board_update()
    

        

        self.assertEqual( self.game.printout(),
        ' *  * |I| * \n'+
        ' *  * |I| * \n'+
        ' *  * |I| * \n'+
        ' *  * |I| * ')
        
        

    
        

if __name__ == '__main__':
    unittest.main()
