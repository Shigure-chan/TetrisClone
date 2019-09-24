import arcade
import gamestate


TITLE = "Tetris"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

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
    'I': (0, 255, 255),  #TEAL
    'J': (0, 51, 204),  #DARK BLUE
    'L': (255, 153, 51),  #ORANGE
    'S': (51, 153, 51),  #GREEN,
    'Z': (255, 51, 0)  #RED,
}

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
            start_y = 0.7 * WINDOW_HEIGHT,
            color = BLACK,
            font_size = 200, 
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
            def left_edge(coords: [int, int]) -> float:
                '''
                returns the number needed for the left edge in arcade.draw_lrtb_rectangle_filled
                '''
                return (MARGIN * WINDOW_WIDTH) + ( (SCORE_LEFT_BOUNDARY - GAP - MARGIN) * ( coords[1] / 10) * WINDOW_WIDTH)
                
            def right_edge(coords: [int, int]) -> float:
                '''
                same thing as left_edge
                '''
                return (MARGIN * WINDOW_WIDTH) + ( (SCORE_LEFT_BOUNDARY - GAP - MARGIN) * ( (1 + coords[1]) / 10) * WINDOW_WIDTH)
            
            def top_edge(coords: [int, int]) -> float:
                '''
                same thing as left_edge
                '''
                return ( (1 - MARGIN) * WINDOW_HEIGHT ) - ( (1 - (2 * MARGIN)) * ((coords[0]-2) / 20) * WINDOW_HEIGHT)
                
            def bottom_edge(coords: [int, int]) -> float:
                '''
                same thing as left_edge
                '''
                return ( (1 - MARGIN) * WINDOW_HEIGHT ) - ( (1 - (2 * MARGIN)) * ((coords[0]-2+1) / 20) * WINDOW_HEIGHT)
            
            def block_render():
                print(self.game.existing_blocks_list())
                for i in self.game.existing_blocks:
                    for j in i.blocks.values():
                        if j[0] >= 2:
                            arcade.draw_lrtb_rectangle_filled(
                                left=left_edge(j), 
                                right=right_edge(j), 
                                top=top_edge(j), 
                                bottom=bottom_edge(j), 
                                color=BLOCK_COLORS[i.block_type]
                                )
            
            block_render()
            
            
            
            
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
        print(symbol)
    
    def on_update(self, delta_time):
        if self.within_game_flag == True:
            self.game.gravity() #blocks fall, land, freeze
            self.game.board_update() #board does any updates
            self.game.mark_lines()
                #print(a.hard_drop_coords()) #test ghost block
                #print(a.printout())
            print(self.game.ghost_printout())
            self.game.line_clear()
        
            if self.game.block.frozen == True:
                self.game.spawn()
        
            

    
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