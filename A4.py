import os
import itertools

from helper import get_user_input, get_example_txt

EXAMPLES_PATH = os.path.join(os.path.dirname(__file__), "A4")


def calculate_element(element: str, last_element: str, calculation_table, row_index, column_index):
    """Berechnet den Wahrheitswehrt für das gegebene Element mit der zusätzlichen Information des letzten Elements. Speichert den Wahrheitswert in calculation_table und gibt das neue letzte Element zurück

    :param element: Das aktuelle Element
    :param last_element: Das letzte Element
    :param calculation_table: Die Tabelle mit den Wahrheitswerten. Wird direkt verändert
    :param row_index: Die aktuelle Zeile
    :param column_index: Die aktuelle Spalte
    :returns: Das neue letzte Element
    """
    if last_element:
        match element:
            case "W":
                if last_element == "W":
                    calculation_table[row_index][column_index] = calculation_table[row_index][column_index - 1] = not (
                        calculation_table[row_index - 1][column_index]
                        and calculation_table[row_index - 1][column_index - 1]
                    )  # NAND
                    element = ""
            case "R":
                if last_element == "r":
                    calculation_table[row_index][column_index] = calculation_table[row_index][column_index - 1] = not (
                        calculation_table[row_index - 1][column_index]
                    )
                    # NOT
                    element = ""
            case "r":
                if last_element == "R":
                    calculation_table[row_index][column_index] = calculation_table[row_index][column_index - 1] = not (
                        calculation_table[row_index - 1][column_index - 1]
                    )
                    # NOT
                    element = ""
            case "B":
                if last_element == "B":
                    calculation_table[row_index][column_index] = calculation_table[row_index - 1][column_index]
                    calculation_table[row_index][column_index - 1] = calculation_table[row_index - 1][column_index - 1]
                    # EQUAL
                    element = ""

    if element.startswith("L"):
        calculation_table[row_index][column_index] = calculation_table[row_index - 1][column_index]
        # EQUAL
    return element


def main():
    """Löst die Aufgabe A4 des Bwinf 42"""
    own_examples, num_examples = get_user_input("nandu", EXAMPLES_PATH)

    for x in range(0, num_examples):
        # Input
        if own_examples:
            raw_data = get_example_txt(f"nanduSelf{x+1}.txt", EXAMPLES_PATH)
            print(f"Eigenes Beispiel {x+1}:")
        else:
            raw_data = get_example_txt(f"nandu{x+1}.txt", EXAMPLES_PATH)
            print(f"Beispiel {x+1}:")

        raw_data.pop(0)  # not needed
        table: list[list[str]] = []  # Pseudocode: BLOCK_TABLE
        for row in raw_data:  # Pseudocode: AufgabeEinlesenZuBlockArray
            table.append(row.split())

        # initialize Qs and Ls
        num_q = 0
        indecies_q = []
        indecies_l = []
        for row_index, _ in enumerate(table):
            for column_index, element in enumerate(table[row_index]):  # first row
                if element.startswith("Q"):
                    num_q += 1
                    indecies_q.append((row_index, column_index))
                elif element.startswith("L"):
                    indecies_l.append((row_index, column_index))

        possible_q_combinations = list(itertools.product([False, True], repeat=num_q))

        for possible_q_combination in possible_q_combinations:
            # this table saves the booleans for the light outputs
            # Psuedocode: CALC_TABLE
            calculation_table = [[None for _ in range(len(table[0]))] for _ in range(len(table))]

            # print Qs
            for num_of_possible_q, possible_q_value in enumerate(possible_q_combination):
                # start printing table
                print(f"Q{num_of_possible_q+1}: {possible_q_value}", end=" ")
                # add the current value of true or false for
                # each Q so that we have all combinations in the end
                calculation_table[indecies_q[num_of_possible_q][0]][
                    indecies_q[num_of_possible_q][1]
                ] = possible_q_combination[num_of_possible_q]

            # go trough each row
            # and compute the bool values for the light outputs
            for row_index, _ in enumerate(table):
                last_element = (
                    None  # last element has to be reset, else it will think that blocks on the edge span over 2 rows
                )
                for column_index, element in enumerate(table[row_index]):
                    # Pseudocode: BerechneBlock
                    last_element = calculate_element(element, last_element, calculation_table, row_index, column_index)

            # print light output
            for num_current_l, (row_index, column_index) in enumerate(indecies_l):
                print(
                    f"L{num_current_l+1}: {calculation_table[row_index][column_index]}",
                    end=" ",
                )

            print()

        print()


if __name__ == "__main__":
    main()
