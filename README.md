# Procedurally Generated Universe
## Inspiration
Where else but YouTube? Credit goes to One Lone Coder for this idea (https://youtu.be/ZZY9YE7rZJw). He implemented it in C++,
but I'm more comfortable with Python.

## Implementation
* Universe Generation
    * I'll be using the Lehmer 64-bit generator to generate pseudo-random numbers.
    * These random numbers will control the existence of a star system in a certain sector.
    * More numbers will be generated concerning the number of planets, the ecosystems of said planets, number of moons, etc.
* Graphics
    * I'll be using Python Arcade (https://arcade.academy/index.html). I settled on this because pygame, tkinter, and graphics.py couldn't achieve smooth enough motion.
    * I WANT COOL WHIP SMOOTH MOTION
    * Haven't figured out this part yet!
