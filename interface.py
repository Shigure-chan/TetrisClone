import arcade
import gamestate
import numbers


TITLE = "Tetris"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700

HORIZONTAL_CENTER = 0.5 * WINDOW_WIDTH

#Makes it so the button sizes are easy to change
BUTTON_TOP_COEFFICIENT = 0.50
INTERVAL_BETWEEN_BUTTONS = 0.15
BUTTON_WIDTH_COEFFICIENT = 0.4 

#Makes it so the text sizes are easy to change
TEXT_BEGINNING_COEFFICIENT = BUTTON_WIDTH_COEFFICIENT - 0.05
TEXT_TOP_COEFFICIENT = BUTTON_TOP_COEFFICIENT - 0.02
INTERVAL_BETWEEN_TEXT = INTERVAL_BETWEEN_BUTTONS

BACKGROUND_COLOUR = (196, 216, 237)
BLACK = (0, 0, 0)

#MENU BUTTONS
BUTTON_BLUE = (0, 204, 255)
BUTTON_BLUE_HIGHLIGHTED = (0, 102, 257)

#MENU BUTTON TEXT
TEXT_COLOR = BLACK
TEXT_COLOR_HIGHLIGHTED = (255, 51, 51)

#BLOCK_COLORS
BLOCK_COLORS = {
    'O': (255, 255, 0),  #YELLOW
    'T': (153, 0, 153),  #PURPLE
    'I': (0, 153, 204),  #TEAL
    'J': (0, 51, 204),  #DARK BLUE
    'L': (255, 153, 51),  #ORANGE
    'S': (51, 153, 51),  #GREEN,
    'Z': (255, 51, 0)  #RED,
}

#GRID_COLOR
GRID_COLOR = (102, 102, 53) #GRAY

#ACTUAL GAME
MARGIN = 0.03
SCORE_LEFT_BOUNDARY = 0.72
GAP = 0.04

class Game(arcade.Window):

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)

        # Set the background color
        arcade.set_background_color(BACKGROUND_COLOUR)

        #Flags...
        self.menu_flag = True
        self.options_flag = False
        self.within_game_flag = False
        
        #Button Highlighting
        self.highlight_play = False
        self.highlight_options = False
        self.highlight_quit = False

        #Game stuff
        self.game = gamestate.GameState()
        self.level = self.game.player_data['level']
        
        self.ticks = 0 #basically a clock

        self.key_down_held = False
        self.duration = 0 #only used when holding DOWN
        
        
        
    def on_draw(self):
        '''
        Functions inside

        main_menu()
            -play_button()
            -options_button()
            -quit_button()
            
        -within_game()
            -left_edge()
            -right_edge()
            -top_eedge()
            -bottom_edge()
        '''
        arcade.start_render()
        
        #MENU
        def main_menu():
            #TITLE
            arcade.draw_text(
            text = "TETRIS", 
            start_x = 0.1 * WINDOW_WIDTH, 
            start_y = 0.65 * WINDOW_HEIGHT,
            color = BLACK,
            font_size = 180, 
            width = int(0.8 * WINDOW_WIDTH),
            align = 'center', 
            font_name=('calibri', 'arial'), 
            bold = True, 
            italic = False, 
            anchor_x = 'left', 
            anchor_y = 'baseline', 
            rotation = 0)

            #Play Button

            def play_button(button_color, text_color):
                arcade.draw_rectangle_filled(
                    center_x = HORIZONTAL_CENTER,
                    center_y = BUTTON_TOP_COEFFICIENT * WINDOW_HEIGHT,
                    width = BUTTON_WIDTH_COEFFICIENT * WINDOW_WIDTH,
                    height = 0.1 * WINDOW_HEIGHT,
                    color = button_color,
                    tilt_angle=0)

                arcade.draw_text(
                    text = "PLAY", 
                    start_x = TEXT_BEGINNING_COEFFICIENT * WINDOW_WIDTH, 
                    start_y = TEXT_TOP_COEFFICIENT * WINDOW_HEIGHT,
                    color = text_color,
                    font_size = 36, 
                    width = int(0.3 * WINDOW_WIDTH),
                    align = 'center', 
                    font_name=('calibri', 'arial'), 
                    bold = True, 
                    italic = False, 
                    anchor_x = 'left', 
                    anchor_y = 'baseline', 
                    rotation = 0)

            def options_button(button_color, text_color):
                #Options Button
                arcade.draw_rectangle_filled(
                    center_x = HORIZONTAL_CENTER, 
                    center_y = (BUTTON_TOP_COEFFICIENT - INTERVAL_BETWEEN_BUTTONS) * WINDOW_HEIGHT, 
                    width = BUTTON_WIDTH_COEFFICIENT * WINDOW_WIDTH, 
                    height = 0.1 * WINDOW_HEIGHT, 
                    color = button_color, 
                    tilt_angle=0)

                arcade.draw_text(
                    text = "OPTIONS", 
                    start_x = TEXT_BEGINNING_COEFFICIENT * WINDOW_WIDTH, 
                    start_y = (TEXT_TOP_COEFFICIENT - INTERVAL_BETWEEN_TEXT) * WINDOW_HEIGHT,
                    color = text_color,
                    font_size = 36, 
                    width = int(0.3 * WINDOW_WIDTH),
                    align = 'center', 
                    font_name=('calibri', 'arial'), 
                    bold = True, 
                    italic = False, 
                    anchor_x = 'left', 
                    anchor_y = 'baseline', 
                    rotation = 0)

            def quit_button(button_color, text_color):
                #Quit Button
                arcade.draw_rectangle_filled(
                    center_x = HORIZONTAL_CENTER, 
                    center_y = (BUTTON_TOP_COEFFICIENT - (2 * INTERVAL_BETWEEN_BUTTONS)) * WINDOW_HEIGHT, 
                    width = BUTTON_WIDTH_COEFFICIENT * WINDOW_WIDTH, 
                    height = 0.1 * WINDOW_HEIGHT, 
                    color = button_color, 
                    tilt_angle=0)

                arcade.draw_text(
                    text = "QUIT", 
                    start_x = TEXT_BEGINNING_COEFFICIENT * WINDOW_WIDTH, 
                    start_y = (TEXT_TOP_COEFFICIENT - ( 2 * INTERVAL_BETWEEN_TEXT)) * WINDOW_HEIGHT,
                    color = text_color,
                    font_size = 36, 
                    width = int(0.3 * WINDOW_WIDTH),
                    align = 'center', 
                    font_name=('calibri', 'arial'), 
                    bold = True, 
                    italic = False, 
                    anchor_x = 'left', 
                    anchor_y = 'baseline', 
                    rotation = 0)

            if self.highlight_play == True:
                play_button(BUTTON_BLUE_HIGHLIGHTED, TEXT_COLOR_HIGHLIGHTED)
            else:
                play_button(BUTTON_BLUE, TEXT_COLOR)
            
            if self.highlight_options == True:
                options_button(BUTTON_BLUE_HIGHLIGHTED, TEXT_COLOR_HIGHLIGHTED)
            else:
                options_button(BUTTON_BLUE, TEXT_COLOR)
            
            if self.highlight_quit == True:
                quit_button(BUTTON_BLUE_HIGHLIGHTED, TEXT_COLOR_HIGHLIGHTED)
            else:
                quit_button(BUTTON_BLUE, TEXT_COLOR)
    
        def within_game():

            def main_boxes():
                #FIELD
                arcade.draw_lrtb_rectangle_outline(
                    left = MARGIN * WINDOW_WIDTH,
                    right = (SCORE_LEFT_BOUNDARY - GAP) * WINDOW_WIDTH,
                    top = (1 - MARGIN) * WINDOW_HEIGHT, 
                    bottom = MARGIN * WINDOW_HEIGHT,
                    color = BLACK, 
                    border_width = 3 
                    )
                
                #SCORE TAB
                arcade.draw_lrtb_rectangle_outline(
                    left = SCORE_LEFT_BOUNDARY * WINDOW_WIDTH,
                    right = (1 - MARGIN) * WINDOW_WIDTH,
                    top = (1 - MARGIN) * WINDOW_HEIGHT, 
                    bottom = MARGIN * WINDOW_HEIGHT,
                    color = BLACK, 
                    border_width = 3 
                    )
            
            #BLOCKS!!!!!
            def left_edge(column: int) -> float:
                '''
                returns the number needed for the left edge in arcade.draw_lrtb_rectangle_filled
                '''
                return (MARGIN * WINDOW_WIDTH) + ( (SCORE_LEFT_BOUNDARY - GAP - MARGIN) * ( column / 10) * WINDOW_WIDTH)
                
            def right_edge(column: int) -> float:
                '''
                same thing as left_edge
                '''
                return (MARGIN * WINDOW_WIDTH) + ( (SCORE_LEFT_BOUNDARY - GAP - MARGIN) * ( (1 + column) / 10) * WINDOW_WIDTH)
            
            def top_edge(row: int) -> float:
                '''
                same thing as left_edge
                '''
                return ( (1 - MARGIN) * WINDOW_HEIGHT ) - ( (1 - (2 * MARGIN)) * ((row-2) / 20) * WINDOW_HEIGHT)
                
            def bottom_edge(row: int) -> float:
                '''
                same thing as left_edge
                '''
                return ( (1 - MARGIN) * WINDOW_HEIGHT ) - ( (1 - (2 * MARGIN)) * ((row-2+1) / 20) * WINDOW_HEIGHT)
            
            def grid_render():
                '''
                renders the grid
                '''
                horizontal_grid = [(left_edge(i), (1 - MARGIN) * WINDOW_HEIGHT, MARGIN * WINDOW_HEIGHT) for i in range(1, 10)]
                
                for i in range(len(horizontal_grid)):
                    arcade.draw_line(
                        start_x=horizontal_grid[i][0],
                        start_y=horizontal_grid[i][1],
                        end_x=horizontal_grid[i][0],
                        end_y=horizontal_grid[i][2],
                        color=GRID_COLOR,
                        line_width=1
                    )
                
                vertical_grid = [(MARGIN * WINDOW_WIDTH, bottom_edge(i), (SCORE_LEFT_BOUNDARY - GAP) * WINDOW_WIDTH) for i in range(2, 21)]

                for i in range(len(vertical_grid)):
                    arcade.draw_line(
                        start_x=vertical_grid[i][0],
                        start_y=vertical_grid[i][1],
                        end_x=vertical_grid[i][2],
                        end_y=vertical_grid[i][1],
                        color=GRID_COLOR,
                        line_width=1
                    )
                
            def block_render():
                '''
                renders all blocks that currently exist in the game...
                '''
                for i in self.game.existing_blocks:
                    for j in i.blocks.values():
                        if j[0] >= 2:
                            arcade.draw_lrtb_rectangle_filled(
                                left=left_edge(j[1]), 
                                right=right_edge(j[1]), 
                                top=top_edge(j[0]), 
                                bottom=bottom_edge(j[0]), 
                                color=BLOCK_COLORS[i.block_type]
                                )
            
            def current_block():
                pass

            def show_queue():
                pass

            
            block_render()
            grid_render()
            main_boxes()
            
            
            
            
        #main_menu() function ends here
        if self.menu_flag == True and self.within_game_flag == False and self.options_flag == False:
            main_menu()
        elif self.within_game_flag == True:
            within_game()
        
            
    
    def on_mouse_press(self, x, y, button, modifiers):
        print(x, y, button)
        
        if within_quit(x,y) and button == arcade.MOUSE_BUTTON_LEFT:
            arcade.close_window()
        
        elif within_play(x,y) and button == arcade.MOUSE_BUTTON_LEFT:
            self.menu_flag = False
            self.options_flag = False
            self.game_setup()
            self.within_game_flag = True

            


            

        elif within_options(x,y) and button == arcade.MOUSE_BUTTON_LEFT:
            self.menu_flag = False
            self.within_game_flag = False
            self.options_flag = True
    
    def game_setup(self):
        '''
        Only executed once when the within_game_flag is set to true
        '''
        self.game.spawn()
        self.game.board_update()
            
    def on_key_press(self, symbol, modifiers):
        if self.within_game_flag == True:
            if symbol == arcade.key.LEFT:
                self.game.move_left()
                self.game.board_update()
            
            if symbol == arcade.key.RIGHT:
                self.game.move_right()
                self.game.board_update()
            
            if symbol == arcade.key.L:
                self.game.rotation(value=-1)
                self.game.board_update()

            if symbol == arcade.key.R:
                self.game.rotation(value=1)
                self.game.board_update()
            
            if symbol == arcade.key.SPACE:
                self.game.hard_drop()
                self.game.board_update()

            if symbol == arcade.key.DOWN:
                self.game.gravity()
                self.game.board_update()
                self.key_down_held = True        

            #this is for debug purposes
            if symbol == arcade.key.E:
                if self.level < 15:
                    self.level += 1
                print(f"Level {self.level}")
    
    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.DOWN:
            self.key_down_held = False
            print(f'Duration {self.duration}')
            self.duration = 0

            
            
                
                
                
            
            
    
    def on_update(self, delta_time):
        def gravity():
            self.game.gravity() #blocks fall, land, freeze
            self.game.board_update() #board does any updates
            self.game.mark_lines()
            #print(a.hard_drop_coords()) #test ghost block
            #print(a.printout())
            print(self.game.ghost_printout())
            print()
            self.game.line_clear()
            self.game.lock_out() #we can make this far mor sophisticated but this seems like a good start.
            
            if self.game.block.frozen == True:
                self.game.spawn()


        if self.within_game_flag == True:
            def block_fall():
                '''
                called four times a frame
                '''
                if self.ticks / 240 >= self.fall_speed(): 
                    gravity()
                    self.ticks = 0

            def key_down():
                if self.key_down_held == True:
                    self.duration += 1

                if self.duration / 240 >= self.soft_drop_speed():
                    gravity()

            self.ticks += 1
            key_down()
            block_fall()

            self.ticks += 1
            key_down()
            block_fall()

            self.ticks += 1
            key_down()
            block_fall()

            self.ticks += 1
            key_down()
            block_fall()
            
            
            

            

    
    def on_mouse_motion(self, x, y, dx, dy):

        if within_play(x,y):
            self.highlight_play = True
        else:
            self.highlight_play = False
        
        if within_options(x,y):
            self.highlight_options = True
        else:
            self.highlight_options = False
        
        if within_quit(x,y):
            self.highlight_quit = True
        else:
            self.highlight_quit = False
    
    def fall_speed(self) -> float:
        '''
        returns the amount of seconds it takes for a block to fall one line based on the current level
        '''
        return round( (0.8 - ((self.level - 1) * 0.007)) ** (self.level-1), 3)
    
    def soft_drop_speed(self) -> float:
        '''
        returns the amount of second it takes for a block to fall one line based on the current level while soft dropping
        '''
        return self.fall_speed() / 20
        


def coordinate_generator(x, y, center_x, center_y, width, height):
    '''
    detects whether a given coordinate is within the boundary of a rectangle or square--given the width, center, and height of the square
    '''
    lower_y = center_y - (height / 2)
    upper_y = center_y + (height / 2)
  
    lower_x = center_x - (width / 2)
    upper_x = center_x + (width / 2)

    within_x = lower_x <= x <= upper_x
    within_y = lower_y <= y <= upper_y

    return within_x and within_y

def within_play(x,y) -> bool:
    center_x = HORIZONTAL_CENTER 
    center_y = BUTTON_TOP_COEFFICIENT * WINDOW_HEIGHT
    width = BUTTON_WIDTH_COEFFICIENT * WINDOW_WIDTH
    height = 0.1 * WINDOW_HEIGHT 
    return coordinate_generator(x,y, center_x, center_y, width, height)
            
def within_options(x,y) -> bool:
    center_x = HORIZONTAL_CENTER
    center_y = (BUTTON_TOP_COEFFICIENT - INTERVAL_BETWEEN_BUTTONS) * WINDOW_HEIGHT
    width = BUTTON_WIDTH_COEFFICIENT * WINDOW_WIDTH
    height = 0.1 * WINDOW_HEIGHT
    return coordinate_generator(x,y, center_x, center_y, width, height)

def within_quit(x,y) -> bool:
    center_x = HORIZONTAL_CENTER
    center_y = (BUTTON_TOP_COEFFICIENT - (2 * INTERVAL_BETWEEN_BUTTONS)) * WINDOW_HEIGHT
    width = BUTTON_WIDTH_COEFFICIENT * WINDOW_WIDTH
    height = 0.1 * WINDOW_HEIGHT
    return coordinate_generator(x,y, center_x, center_y, width, height)



def main():
    window = Game(WINDOW_WIDTH, WINDOW_HEIGHT, "TETRIS")
    
    arcade.run()


if __name__ == "__main__":
    main()