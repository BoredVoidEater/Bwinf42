"""Löst die Aufgabe J2 des Bwinf 42"""

import os

from helper import get_user_input, get_example_image

EXAMPLES_PATH = os.path.dirname(__file__)


def main():
    """Löst die Aufgabe J2 des Bwinf 42"""
    own_examples, num_examples = get_user_input("bild", EXAMPLES_PATH)
    for examples in range(0, num_examples):
        # Input
        if own_examples:
            raw_data = get_example_image(f"bildSelf{examples+1}.png", EXAMPLES_PATH)
        else:
            raw_data = get_example_image(f"bild{examples+1}.png", EXAMPLES_PATH)

        img = raw_data.load()

        print(f"Beispiel {examples+1}:")

        width, height = raw_data.size

        r, g, b = img[0, 0]
        pos = [0, 0]

        msg = chr(img[0, 0][0])

        while not (g == 0 and b == 0):
            pos[0] += g
            pos[1] += b

            r, g, b = img[pos[0] % width, pos[1] % height]

            msg += chr(r)

        print(msg)

        raw_data.close()

        print()


if __name__ == "__main__":
    main()
