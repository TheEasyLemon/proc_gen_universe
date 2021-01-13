"""
Arcade program that uses the classes in universe.py
Inspired by the One Lone Coder's video on Procedurally Generated Universes
"""

# Imports
import arcade
from copy import deepcopy
from universe import StarSystem
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

# Constants
SECTOR_SIZE = 50
SECTORS_X = SCREEN_WIDTH / SECTOR_SIZE
SECTORS_Y = SCREEN_HEIGHT / SECTOR_SIZE
SCREEN_TITLE = "Dawson's Universe"
MOVEMENT_SPEED = 1
UNIVERSE_SIZE = 10
DECELERATION = 0.05

# Check SECTORS_X and SECTORS_Y are equal, comparing float to int
if int(SECTORS_X) != SECTORS_X or int(SECTORS_Y) != SECTORS_Y:
    raise Exception("Adjust screen width, height, or sector size")
else:
    SECTORS_X = int(SECTORS_X)
    SECTORS_Y = int(SECTORS_Y)


class StartView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.COOL_GREY)
        # load the game in the background when we show
        self.game_view = UniverseGame()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Dawson's Universe", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.window.show_view(self.game_view)


class UniverseGame(arcade.View):
    """User starts with a black screen with random stars around.
    Navigation with WASD, new stars procedurally generated around.
    Returning to the same galaxy_offset yields the same procedurally
    generated stars."""

    def __init__(self):
        super().__init__()

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        arcade.set_background_color(arcade.color.BLACK)

        # controls the place you're shown within the entire galaxy
        # starts in the middle of the galaxy
        self.galaxy_offset = {"x": -(UNIVERSE_SIZE * SCREEN_WIDTH / 2),
                              "y": -(UNIVERSE_SIZE * SCREEN_HEIGHT / 2),
                              "dx": 0,
                              "dy": 0}

        # the star being hovered over
        self.hovered_star = None

        # which star the user clicked on
        self.selected_star = None

        # list of all visible stars' VBOs
        self.star_list = arcade.ShapeElementList()
        # two dimensional array of StarSystem objects
        self.universe = []

        self.generate_star_list()

    def generate_star_list(self):
        new_universe = []
        new_star_list = arcade.ShapeElementList()

        # procedurally generate all the StarSystem objects on the screen and store as VBOs
        for x in range(0, SECTORS_X):
            # a row of sectors, will be appended to self.universe
            row = []
            for y in range(0, SECTORS_Y):
                seed_x = int(self.galaxy_offset["x"]) + x
                seed_y = int(self.galaxy_offset["y"]) + y

                s = StarSystem(seed_x, seed_y)
                row.append(s)

                if s.star_exists:
                    star = arcade.create_ellipse_filled(x * SECTOR_SIZE,
                                                        y * SECTOR_SIZE,
                                                        s.star_diameter,
                                                        s.star_diameter,
                                                        s.star_color)
                    new_star_list.append(star)

            new_universe.append(row)

        self.universe = new_universe
        self.star_list = new_star_list

    def draw_selection_circle(self, star):
        arcade.draw_circle_outline(star.x,
                                   star.y,
                                   star.star_diameter + 10,
                                   arcade.color.YELLOW)

    def draw_star_menu(self, star):
        # menu that shows up when you click on a star
        star_menu = arcade.ShapeElementList()
        outer = arcade.create_rectangle_filled(SCREEN_WIDTH / 2,
                                               SCREEN_HEIGHT / 4,
                                               SCREEN_WIDTH - 30,
                                               (SCREEN_HEIGHT / 2) - 30,
                                               arcade.color.AIR_FORCE_BLUE)
        star_menu.append(outer)
        inner = arcade.create_rectangle_filled(SCREEN_WIDTH / 2,
                                               SCREEN_HEIGHT / 4,
                                               SCREEN_WIDTH - 50,
                                               (SCREEN_HEIGHT / 2) - 50,
                                               arcade.color.EERIE_BLACK)
        star_menu.append(inner)
        star_menu.draw()

        arcade.draw_text(str(star),
                         30,
                         (SCREEN_WIDTH / 2) - 30,
                         arcade.color.WHITE,
                         24,
                         anchor_x="left", anchor_y="top")

        self.planet_list.draw()

    def on_draw(self):
        """Called whenever you draw your window, about every 10 ms"""
        # Clear the screen and start drawing
        arcade.start_render()

        # draw star_list
        self.star_list.draw()

        if self.hovered_star is not None:
            self.draw_selection_circle(self.hovered_star)

        if self.selected_star is not None:
            self.draw_selection_circle(self.selected_star)

        if self.selected_star is not None:
            self.draw_star_menu(self.selected_star)

    def on_update(self, delta_time: float):
        """Handles the screen that pops up for selected stars
        Also regenerates data for star_list when player moves"""
        # regenerate the data in self.star_list and self.universe as you move
        self.generate_star_list()

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

        # Calculate dy and dx
        if self.up_pressed and not self.down_pressed:
            self.galaxy_offset["dy"] = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.galaxy_offset["dy"] = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.galaxy_offset["dx"] = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.galaxy_offset["dx"] = MOVEMENT_SPEED

        # Adjust galaxy_offset based on dy and dx
        self.galaxy_offset["x"] += self.galaxy_offset["dx"]
        self.galaxy_offset["y"] += self.galaxy_offset["dy"]

    def on_key_press(self, symbol: int, modifiers: int):
        """Handles keypress events, WASD to move"""
        if symbol == 119:  # "w"
            self.up_pressed = True
        elif symbol == 97:  # "a"
            self.left_pressed = True
        elif symbol == 115:  # "s"
            self.down_pressed = True
        elif symbol == 100:  # "d"
            self.right_pressed = True
        elif symbol == 103:  # "g"
            print(self.galaxy_offset)
        elif symbol == 104:  # "h"
            print(self.hovered_star is not None)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == 119:  # "w"
            self.up_pressed = False
        elif symbol == 97:  # "a"
            self.left_pressed = False
        elif symbol == 115:  # "s"
            self.down_pressed = False
        elif symbol == 100:  # "d"
            self.right_pressed = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """Called when the user moves the mouse, handles the appearance of
        a selection circle when you hover over a sector that contains a star
        """
        # Assumed nothing is hovered until found
        self.hovered_star = None

        # get the sector where the mouse is
        x_sector = int(x // SECTOR_SIZE)
        y_sector = int(y // SECTOR_SIZE)

        try:
            current_star = self.universe[x_sector][y_sector]
        except IndexError:
            print(f"{x_sector}x, {y_sector}y")

        # check whether the current sector that the mouse is in has a star
        if current_star.star_exists:
            self.hovered_star = current_star

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Called when the mouse is pressed"""
        if self.hovered_star is not None:
            # generate the system
            self.hovered_star.generate_system()
            # copy the state of the newly generated star system
            self.selected_star = deepcopy(self.hovered_star)

            # create ShapeElementList of all of the planets surrounding the star
            self.planet_list = arcade.ShapeElementList()
            for p in self.selected_star.planets:
                planet = arcade.create_ellipse_filled(p.distance,
                                                      SCREEN_HEIGHT / 4,
                                                      p.diameter,
                                                      p.diameter,
                                                      p.color)
                self.planet_list.append(planet)
        else:
            self.selected_star = None


if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = StartView()
    window.show_view(view)
    arcade.run()
    arcade.close_window()
