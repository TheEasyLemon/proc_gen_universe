# Procedurally Generated Universe
## Inspiration
Where else but YouTube? Credit goes to One Lone Coder for this idea (https://youtu.be/ZZY9YE7rZJw). He implemented it in C++,
but I'm more comfortable with Python.

## Implementation
* Universe Generation
    * I'll be using the Lehmer 64-bit generator to generate pseudo-random numbers.
    * These random numbers will control the existence of a star system in a certain sector.
    * More numbers will be generated concerning the number of planets, the ecosystems of said planets, number of moons, etc.
    * I won't be procedurally generating the planets as I find it's a little too slow for Python. Instead, I'll be loading a certain size universe and then loading more "chunks" as we go further.
* Graphics
    * I'll be using Python Arcade (https://arcade.academy/index.html). I settled on this because pygame, tkinter, and graphics.py couldn't achieve smooth enough motion.
    * The key is to use Vertex Buffer Objects (VBOs) because they provide much greater performance than drawing a bunch of planets.