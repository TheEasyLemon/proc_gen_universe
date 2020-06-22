import math
import random
from planet_name_generator import generate_name


class Planet:
    def __init__(self):
        self.distance = 0
        self.diameter = 0
        self.foliage = 0
        self.minerals = 0
        self.water = 0
        self.gases = 0
        self.temperature = 0
        self.population = 0
        self.ring = False
        self.moons = []

    def __str__(self):
        s = ""
        for name, val in vars(self).items():
            s += f"{name}: {val}\n"
        return s

    def __repr__(self):
        return self.__str__()


class StarSystem:
    def __init__(self, x, y, gen_full_system=False):
        self.x = x
        self.y = y
        self.gen_full_system = gen_full_system
        self.planets = []

        self.name = generate_name()

        # set random seed based on location and random noise
        self.seed = ((self.x + random.randint(0, 1000)) & 0xFFFF) << 16 | ((self.y + random.randint(0, 1000)) & 0xFFFF)

        # not all locations have a star
        self.star_exists = (self.rnd_int(0, 20) == 1)
        if not self.star_exists:
            return

        # generate star
        self.star_diameter = self.rnd_int(10, 40)
        self.star_color = (self.rnd_int(40, 255), self.rnd_int(40, 255), self.rnd_int(40, 255))

        # when looking at the galaxy map, we don't need full system
        if not self.gen_full_system:
            return

        self.generate_system()

    def generate_system(self):
        # set gen_full_system to True
        self.gen_full_system = True

        # generate planets
        distance_from_star = self.rnd_double(60, 200)
        num_planets = self.rnd_int(0, 10)

        for i in range(num_planets):
            p = Planet()
            p.distance = distance_from_star
            distance_from_star += self.rnd_int(20, 200)
            p.diameter = self.rnd_int(4, 20)
            # temperature decreases as distance increases
            p.temperature = 10000 / p.distance ** 2
            # foliage is normally distributed, centered on 20 degrees C
            p.foliage = (math.e ** (-0.01 * (p.temperature - 20) ** 2))
            # bigger diameter means more minerals due to the square-cube law
            p.minerals = (p.diameter ** 2) / 400
            # I have no idea...
            p.gases = abs(2 * p.foliage - p.minerals)
            p.water = abs(p.gases - p.minerals) * 3

            # normalize to 100%
            correction_factor = 1 / (p.foliage + p.minerals + p.gases + p.water)
            p.foliage *= correction_factor
            p.minerals *= correction_factor
            p.gases *= correction_factor
            p.water *= correction_factor

            # population is random for now, negative lower bound so
            # 80% of planets have no population
            p.population = max(self.rnd_int(-20000000, 5000000), 0)

            # 20% of planets have a ring
            p.ring = (self.rnd_int(0, 10) == 1)

            num_moons = max(self.rnd_int(-5, 5), 0)
            # a moon is just a diameter for now
            for j in range(num_moons):
                p.moons.append(self.rnd_int(1, 5))

            self.planets.append(p)

    def rnd(self):
        # Lehmer 64-bit generator
        self.seed = (self.seed * 48271) % 0x7fffffff
        return self.seed

    def rnd_int(self, mi, ma):
        return (self.rnd() % (ma - mi)) + mi

    def rnd_double(self, mi, ma):
        """DEPRECATED"""
        return (self.rnd() / 2147483647) * (ma - mi)

    def __str__(self):
        return f"Welcome to {self.name}!"

    def __repr__(self):
        # iterate through vars
        return "".join([f"{name}: {val}\n" for name, val in vars(self).items()])


class Universe:
    def __init__(self, sectors_x, sectors_y, sector_size):
        self.sectors_x = sectors_x
        self.sectors_y = sectors_y
        self.sector_size = sector_size
        self.starsystems = []

        for i in range(sectors_x):
            # appends by rows
            temp = []
            for j in range(sectors_y):
                star = StarSystem(self.sector_size * i, self.sector_size * j)
                temp.append(star)
            self.starsystems.append(temp)
