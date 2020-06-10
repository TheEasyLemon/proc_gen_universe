"""
Arcade program that uses the classes in universe.py
Based off the One Line Coder's video on Procedurally Generated Universes
"""

# Imports
import arcade

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Dawson's Universe"
RADIUS = 150


def main():
    # Open the window and set bkg color
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.BLACK)

    # Clear the screen and start drawing
    arcade.start_render()

    # Blue circle
    arcade.draw_circle_filled(300, 400, RADIUS, arcade.color.BLUE)

    # Finish rendering
    arcade.finish_render()

    # Display everything
    arcade.run()


if __name__ == "__main__":
    main()

