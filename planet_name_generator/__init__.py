import random

SUFFIXES = ["prime", "",
            "B", "",
            "alpha", "",
            'proxima', "",
            "V", "",
            "C", "",
            "X", "",
            "D", "",
            "", ""]  # empty strings so some don't have suffixes

with open("planet_name_generator/planets.txt", "r") as f:
    raw = f.read()
PLANETS = raw.split("\n")

syllables = []

for p in PLANETS:
    lex = p.split("-")
    for syl in lex:
        if syl not in syllables:
            syllables.append(syl)

size = len(syllables)
freq = [[0] * size for i in range(size)]

for p in PLANETS:
    lex = p.split("-")
    i = 0
    while i < len(lex) - 1:
        freq[syllables.index(lex[i])][syllables.index(lex[i+1])] += 1
        i += 1
    freq[syllables.index(lex[len(lex) - 1])][size - 1] += 1


def generate_name():
    planet_name = ""
    length = random.randint(2, 3)
    initial = random.randint(0, size - 1)

    while length > 0:
        while 1 not in freq[initial]:
            initial = random.randint(0, size - 1)
        planet_name += syllables[initial]
        initial = freq[initial].index(1)
        length -= 1

    suffix_index = random.randint(0, len(SUFFIXES) - 1)
    planet_name += f" {SUFFIXES[suffix_index]}"

    return (" ".join([s.capitalize() for s in planet_name.split(" ")])).strip()


if __name__ == "__main__":
    print(generate_name())
