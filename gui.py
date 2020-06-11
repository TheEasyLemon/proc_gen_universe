"""
Arcade program that uses the classes in universe.py
Based off the One Lone Coder's video on Procedurally Generated Universes
"""

# Imports
import arcade
from universe import StarSystem, Planet

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Dawson's Universe"
RADIUS = 150


class UniverseApp(arcade.Window):
    """User starts with a black screen with random stars around.
    Navigation with WASD, new stars procedurally generated around.
    Returning to the same galaxy_offset yields the same procedurally
    generated stars."""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # set up empty sprite list for stars
        self.stars_list = arcade.SpriteList()
        # contains all the stars and the player
        self.all_list = arcade.SpriteList()

        self.setup()

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)

        # controls the place you're shown within the entire galaxy
        self.galaxy_offset = [0, 0]
        # boolean to know when to show star window
        self.starSelected = False
        # holders to generate star seed
        self.selectedStarSeed1 = 0
        self.selectedStarSeed2 = 0

        self.player = arcade.Sprite("images.jpg")

    def on_draw(self):
        """Called whenever you draw your window"""
        # Clear the screen and start drawing
        arcade.start_render()

        # Blue circle
        arcade.draw_circle_filled(300, 400, RADIUS, arcade.color.BLUE)

        # Finish rendering
        arcade.finish_render()

    def on_key_press(self, symbol: int, modifiers: int):
        """Handles keypress events, WASD to move, Q to quit"""
        if symbol == 119:  # "w"
            pass
        if symbol == 97:  # "a"
            pass
        if symbol == 115:  # "s"
            pass
        if symbol == 100:  # "d"
            pass

        if symbol == 113:  # "q" to quit
            pass


if __name__ == "__main__":
    app = UniverseApp(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
