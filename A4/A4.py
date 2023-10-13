import itertools

OWNEXAMPLES = True


def get_example_txt(path: str) -> list[str]:
    """ließt das Beispiel am relativen Pfand ein

    :param path: Der relative pfad von der txt-Datei des Beispiels
    :returns: eine liste von Zeilen des Beispiels
    """
    return [line.strip() for line in open(path).readlines()]


def calculate_element(element: str, last_element: str, calculation_table, row_index, column_index):
    if last_element:
        match element:
            case "W":
                if last_element == "W":
                    calculation_table[row_index][column_index] = calculation_table[row_index][column_index - 1] = not (
                        calculation_table[row_index - 1][column_index]
                        and calculation_table[row_index - 1][column_index - 1]
                    )
                    element = ""
            case "R":
                if last_element == "r":
                    calculation_table[row_index][column_index] = calculation_table[row_index][column_index - 1] = not (
                        calculation_table[row_index - 1][column_index]
                    )
                    element = ""
            case "r":
                if last_element == "R":
                    calculation_table[row_index][column_index] = calculation_table[row_index][column_index - 1] = not (
                        calculation_table[row_index - 1][column_index - 1]
                    )
                    element = ""
            case "B":
                if last_element == "B":
                    calculation_table[row_index][column_index] = calculation_table[row_index - 1][column_index]
                    calculation_table[row_index][column_index - 1] = calculation_table[row_index - 1][column_index - 1]
                    element = ""

    if element.startswith("L"):
        calculation_table[row_index][column_index] = calculation_table[row_index - 1][column_index]

    return element


def main():
    for x in range(2, 3):
        # Input
        if OWNEXAMPLES:
            raw_data = get_example_txt(f"nanduSelf{x+1}.txt")
            print(f"Eigenes Beispiel {x+1}:")
        else:
            raw_data = get_example_txt(f"nandu{x+1}.txt")
            print(f"Beispiel {x+1}:")

        raw_data.pop(0)  # not needed
        table: list[list[str]] = []
        for row in raw_data:
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
                last_element = None
                for column_index, element in enumerate(table[row_index]):
                    last_element = calculate_element(element, last_element, calculation_table, row_index, column_index)

            print(calculation_table)

            # print light output
            for row_index, column_index in indecies_l:
                print(
                    f"{element}: {calculation_table[row_index][column_index]}",
                    end=" ",
                )

            print()

        print()


if __name__ == "__main__":
    main()
