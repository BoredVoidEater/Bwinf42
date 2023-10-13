"""Löst die Aufgabe J1 des Bwinf 42"""

OWNEXAMPLES = True  # True für eigene Beispiele False für originale Beispiele
NUMEXAMPLES = 2


def bag_to_str(bag: dict[int:int]) -> str:
    """mache die Tüte zu einem string in schönem Format und mit Buchstaben als Spiele

    :param bag: die Tüte die zum string gemacht wird
    :returns: den string der Tüte
    """

    bag_unpacked = [
        f"{bag[game]} mal Spiel {chr(game + ord('A'))}"
        for game in bag
        if bag[game] != 0
    ]

    return ", ".join(bag_unpacked)


def get_example_txt(path: str) -> list[str]:
    """ließt das Beispiel am relativen Pfand ein

    :param path: Der relative pfad von der txt-Datei des Beispiels
    :returns: eine liste von Zeilen des Beispiels
    """
    return [line.strip() for line in open(path).readlines()]


def main():
    for examples in range(NUMEXAMPLES):
        # Input
        if OWNEXAMPLES:
            raw_data = get_example_txt(f"wundertueteSelf{examples}.txt")
        else:
            raw_data = get_example_txt(f"wundertuete{examples}.txt")

        print(f"Beispiel {examples+1}:")

        n = int(raw_data[0])
        k = int(raw_data[1])

        # Games
        count = {i: int(gameCount) for i, gameCount in enumerate(raw_data[2 : 2 + k])}

        # Bags
        bags = [{i: 0 for i in range(k)} for _ in range(n)]

        # Calculations
        for game in count:
            evenly_distributable, extra = divmod(count[game], n)
            # distribute the games enough to give everyone
            for bag in bags:
                bag[game] += evenly_distributable

            # sort bags after whole count of games in them min->max
            bags = sorted(bags, key=lambda b: sum(b.values()))

            # give bags with less games in them the extra games left from this game first
            for i in range(extra):
                bags[i][game] += 1

        # Output
        summed_values = [sum(bag.values()) for bag in bags]
        print(
            "Bei der folgenden Lösung unterscheiden sich die Gesamtzahlen der Spiele zwischen je zwei Tüten um höchstens",
            max(summed_values) - min(summed_values),
        )

        last_matching_bag_index: int = -1
        for i, bag in enumerate(bags):
            if (
                last_matching_bag_index != -1 and i < len(bags) - 1
            ):  # we have a last bag and a next bag
                if bag == bags[last_matching_bag_index]:
                    # the bag matches the one/s before
                    if i - last_matching_bag_index <= 2:
                        # the first two repetitions
                        print(f"Tüte {i+1}: wie Tüte {last_matching_bag_index+1}")
                    elif bags[i + 1] != bag:
                        # the last repetition
                        print(f"Tüte {i+1}: wie Tüte {last_matching_bag_index+1}")
                    elif i - last_matching_bag_index == 3:
                        # the third repetition
                        print("...")
                else:
                    # this bag did not match the last one -> just print the whole thing
                    print(f"Tüte {i+1}: ", bag_to_str(bag))
                    last_matching_bag_index = i
            else:
                if i == 0:
                    # we are at the first bag
                    print(f"Tüte {i+1}: ", bag_to_str(bag))
                    last_matching_bag_index = i
                else:
                    # we are at the last bag
                    if bags[last_matching_bag_index] == bag:
                        print(f"Tüte {i+1}: wie Tüte {last_matching_bag_index+1}")
                    else:
                        print(f"Tüte {i+1}: ", bag_to_str(bag))

        print()


if __name__ == "__main__":
    main()
