"""Löst die Aufgabe J1 des Bwinf 42"""

import os

from helper import get_user_input, get_example_txt

EXAMPLES_PATH = os.path.join(os.path.dirname(__file__), "J1")


def bag_to_str(bag: dict[int:int], number_of_games: int) -> str:
    """transformiert die Tüte zu einem string in schönem Format und mit Buchstaben als Spiele

    :param bag: die Tüte die zum string gemacht wird
    :returns: den string der Tüte
    """

    if number_of_games > 25:
        # if there are more than 26 games, we need to use numbers instead of letters for naming them
        bag_unpacked = [f"{bag[game]} mal Spiel {game}" for game in bag if bag[game] != 0]
    bag_unpacked = [f"{bag[game]} mal Spiel {chr(game + ord('A'))}" for game in bag if bag[game] != 0]

    return ", ".join(bag_unpacked)


def print_output(bags, number_of_games):
    """Gibt die Lösung schön formatiert aus

    :param bags: Liste aller Tüten mit den Spielen
    :param number_of_games: Anzahl aller Spiele
    """

    # This is only used for output formatting and adds "wie Tüte x" if the bag is the same as the one before
    last_matching_bag_index: int = -1
    for i, bag in enumerate(bags):
        if last_matching_bag_index != -1 and i < len(bags) - 1:  # we have a last bag and a next bag
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
                print(f"Tüte {i+1}: ", bag_to_str(bag, number_of_games))
                last_matching_bag_index = i
        else:
            if i == 0:
                # we are at the first bag
                print(f"Tüte {i+1}: ", bag_to_str(bag, number_of_games))
                last_matching_bag_index = i
            else:
                # we are at the last bag
                if bags[last_matching_bag_index] == bag:
                    print(f"Tüte {i+1}: wie Tüte {last_matching_bag_index+1}")
                else:
                    print(f"Tüte {i+1}: ", bag_to_str(bag, number_of_games))

    print()


def main():
    """Löst die Aufgabe J1 des Bwinf 42"""

    own_examples, num_examples = get_user_input("wundertuete", EXAMPLES_PATH)

    for examples in range(num_examples):
        # Input
        if own_examples:
            raw_data = get_example_txt(f"wundertueteSelf{examples}.txt", EXAMPLES_PATH)
        else:
            raw_data = get_example_txt(f"wundertuete{examples}.txt", EXAMPLES_PATH)

        print(f"Beispiel {examples+1}:")

        n = int(raw_data[0])
        k = int(raw_data[1])

        # Games
        count = {i: int(gameCount) for i, gameCount in enumerate(raw_data[2 : 2 + k])}
        number_of_games = sum(count.values())

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

        print_output(bags, number_of_games)


if __name__ == "__main__":
    main()
