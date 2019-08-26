'''
Get the game to even display properly...
'''



import gamestate

import arcade

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "PyTris"

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()