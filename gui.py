"""
Arcade program that uses the classes in universe.py
Based off the One Lone Coder's video on Procedurally Generated Universes
"""

# Imports
import arcade
from universe import Universe

# Constants
# Screen Height and Width need to be divisible by SECTOR_SIZE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SECTOR_SIZE = 50
SECTORS_X = int(SCREEN_WIDTH / SECTOR_SIZE)
SECTORS_Y = int(SCREEN_HEIGHT / SECTOR_SIZE)
SCREEN_TITLE = "Dawson's Universe"
SCALING = 0.5
MOVEMENT_SPEED = 7
UNIVERSE_SIZE = 10
DECELERATION = 0.25


class UniverseApp(arcade.Window):
    """User starts with a black screen with random stars around.
    Navigation with WASD, new stars procedurally generated around.
    Returning to the same galaxy_offset yields the same procedurally
    generated stars."""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)

        # controls the place you're shown within the entire galaxy
        self.galaxy_offset = {"x": 0, "y": 0, "dx": 0, "dy": 0}

        # storing whether a star is being hovered over or not
        self.starHovered = False
        self.hovered_x = 0
        self.hovered_y = 0
        self.hovered_diameter = 0
        # boolean to know when to show star window
        self.starSelected = False
        # holders to generate star seed
        self.selectedStarSeed1 = 0
        self.selectedStarSeed2 = 0

        self.universe = Universe(SECTORS_X * UNIVERSE_SIZE, SECTORS_Y * UNIVERSE_SIZE, SECTOR_SIZE)

        # create planet list and populate with random planets
        self.star_list = arcade.ShapeElementList()

        for count_x, star_list in enumerate(self.universe.starsystems):
            for count_y, star in enumerate(star_list):
                if star.star_exists:
                    x_pos = SCREEN_WIDTH / 2 - SECTOR_SIZE * (0.5 * SECTORS_X - count_x)
                    y_pos = SCREEN_HEIGHT / 2 - SECTOR_SIZE * (0.5 * SECTORS_Y - count_y)
                    shape = arcade.create_ellipse_filled_with_colors(x_pos, y_pos, star.star_diameter,
                                                                     star.star_diameter, star.star_color,
                                                                     star.star_color)
                    self.star_list.append(shape)

    def on_draw(self):
        """Called whenever you draw your window, about every 0.8 ms"""
        # Clear the screen and start drawing
        arcade.start_render()

        self.star_list.draw()

        if self.starHovered:
            arcade.draw_circle_outline(self.hovered_x + self.galaxy_offset["x"],
                                       self.hovered_y + self.galaxy_offset["y"],
                                       self.hovered_diameter + 10, arcade.color.YELLOW)

        # green square is the player, which "moves"
        self.player = arcade.draw_rectangle_filled(SCREEN_WIDTH / 2,
                                                   SCREEN_HEIGHT / 2, 10, 10, arcade.color.YELLOW_GREEN)

    def on_update(self, delta_time: float):
        """Handles the screen that pops up for selected stars"""

        # Calculate deceleration
        if abs(self.galaxy_offset["dx"]) > DECELERATION:
            if self.galaxy_offset["dx"] > 0:
                self.galaxy_offset["dx"] -= DECELERATION
            else:
                self.galaxy_offset["dx"] += DECELERATION
        else:
            self.galaxy_offset["dx"] = 0

        if abs(self.galaxy_offset["dy"]) > DECELERATION:
            if self.galaxy_offset["dy"] > 0:
                self.galaxy_offset["dy"] -= DECELERATION
            else:
                self.galaxy_offset["dy"] += DECELERATION
        else:
            self.galaxy_offset["dy"] = 0

        # Notice - movement is opposite of typical
        # We are moving the background, not the player
        if self.up_pressed and not self.down_pressed:
            self.galaxy_offset["dy"] = -MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.galaxy_offset["dy"] = MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.galaxy_offset["dx"] = MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.galaxy_offset["dx"] = -MOVEMENT_SPEED

        # Adjust galaxy_offset
        self.galaxy_offset["x"] += self.galaxy_offset["dx"]
        self.galaxy_offset["y"] += self.galaxy_offset["dy"]

        # Adjust stars relative to galaxy_offset
        self.star_list.center_x = self.galaxy_offset["x"]
        self.star_list.center_y = self.galaxy_offset["y"]

    def on_key_press(self, symbol: int, modifiers: int):
        """Handles keypress events, WASD to move, Q to quit"""
        if symbol == 113:  # "q" to quit
            exit(0)

        if symbol == 119:  # "w"
            self.up_pressed = True
        elif symbol == 97:  # "a"
            self.left_pressed = True
        elif symbol == 115:  # "s"
            self.down_pressed = True
        elif symbol == 100:  # "d"
            self.right_pressed = True

    def on_key_release(self, symbol: int, modifiers: int):
        # Resets speed to 0
        if symbol == 119:  # "w"
            self.up_pressed = False
        elif symbol == 97:  # "a"
            self.left_pressed = False
        elif symbol == 115:  # "s"
            self.down_pressed = False
        elif symbol == 100:  # "d"
            self.right_pressed = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """Called when the user moves the mouse"""
        # boolean to keep track of if a star system is found at the mouse's position
        star_found = False

        # Find star that the mouse is clicking at and update hovered variables so it can be drawn
        for star_list in self.universe.starsystems:
            for star in star_list:
                true_x = star.x + self.galaxy_offset["x"]
                true_y = star.y + self.galaxy_offset["y"]

                # if star exists and you're clicking it
                if star.star_exists:
                    x_hover = abs(x - true_x) < (star.star_diameter / 2)
                    y_hover = abs(y - true_y) < (star.star_diameter / 2)
                    if x_hover and y_hover:
                        star_found = True

                        self.starHovered = True
                        # we record the star's x and y and not the true x and y
                        # so we can update it based on the changing galaxy offset
                        self.hovered_x = star.x
                        self.hovered_y = star.y
                        self.hovered_diameter = star.star_diameter

        if not star_found:
            self.starHovered = False

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Called when the mouse is pressed"""
        pass


if __name__ == "__main__":
    window = UniverseApp(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
    arcade.close_window()
