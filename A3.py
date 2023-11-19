import os
import heapq
import numpy as np
import sys

from helper import get_example_txt, get_user_input

EXAMPLES_PATH = os.path.join(os.path.dirname(__file__), "A3")


# A*
class Node:
    """Eine einfache Node Klasse für backtracking und Cost berechnen, speichert auch die Position

    :var position: Die Position des Nodes
    :var parent: Der Parent Node
    :var cost: Die Kosten um zu diesem Node zu kommen
    """

    def __init__(self, position, parent=None, cost=0):
        self.position = position  # y,x,floor
        self.parent = parent  # parent node
        self.cost = cost  # the basic cost + heuristicCost of this Node

    def __repr__(self) -> str:
        return f"Node: x: {self.position[0]} y: {self.position[1]} floor: {self.position[2]} cost: {self.cost}"

    def __eq__(self, __value: object) -> bool:
        return self.position == __value.position

    def __lt__(self, __value: object) -> bool:
        return self.cost < __value.cost

    def __le__(self, __value: object) -> bool:
        return self.cost <= __value.cost

    def __gt__(self, __value: object) -> bool:
        return self.cost > __value.cost

    def __ge__(self, __value: object) -> bool:
        return self.cost >= __value.cost

    def __hash__(self) -> int:
        return hash(self.position)


def heuristic_cost(nodePos: tuple[int, int, int], goalPos: tuple[int, int, int]) -> int:
    """Berechnet die Heuristik für die Distanz zwischen zwei Punkten

    :param nodePos: Die Position des aktuellen Nodes
    :param goalPos: Die Position des Zielnodes
    :returns: Die estimierten Kosten um von nodePos zu goalPos zu kommen
    """
    x1, y1, f1 = nodePos
    x2, y2, f2 = goalPos

    return abs(x1 - x2) + abs(y1 - y2) + abs(f1 - f2) * 3  # floor change cost is 3


def get_neighbors(node, floors, goalPos: tuple[int, int, int]):
    """Gibt alle Nachbarn eines Nodes zurück

    :param node: Der Node dessen Nachbarn gesucht werden
    :param floors: Die Etagen der Schule als Karte
    :param goalPos: Die Position des Zielnodes
    :returns: Eine Liste aller Nachbarn
    """
    x, y, f = node.position
    neighbors = []

    for ajacent_x, ajacent_y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_x, new_y = x + ajacent_x, y + ajacent_y
        if floors[f][new_x][new_y] != "#":
            neighbors.append(
                Node(
                    (new_x, new_y, f),
                    parent=node,
                    cost=node.cost + 1 + heuristic_cost((new_x, new_y, f), goalPos),
                )
            )

    if floors[1 - f][x][y] != "#":
        neighbors.append(
            Node(
                (x, y, 1 - f),
                parent=node,
                cost=node.cost + 3 + heuristic_cost((x, y, 1 - f), goalPos),
            )
        )  # for two floor 1-f because 0->1 and 1->0

    return neighbors


def a_star(start: Node, goal: Node, floors) -> list[tuple[int, int, int]]:
    """Führt den A* Algorithmus aus

    :param start: Der Startnode
    :param goal: Der Zielnode
    :param floors: Die Etagen der Schule als Karte
    :returns: Der Pfad von start zu goal
    """
    queque = []
    explored = set()

    heapq.heappush(queque, start)

    while queque:
        curNode: Node = heapq.heappop(queque)

        if curNode == goal:
            # Goal reached, construct and return the path
            path: list[tuple[int, int, int]] = []
            while curNode:
                # backtrack back to start
                path.append(curNode.position)
                curNode = curNode.parent
            return path[::-1]  # reverse because we backtracked from end

        # we have now seen this node
        explored.add(curNode)

        for neighbor in get_neighbors(curNode, floors, goal.position):
            if neighbor in explored:
                # already seen dont care
                continue

            if neighbor not in queque:
                heapq.heappush(queque, neighbor)


def main():
    """Löst die Aufgabe A3 des Bwinf 42"""
    own_examples, num_examples = get_user_input("zauberschule", EXAMPLES_PATH)

    for x in range(num_examples):
        if own_examples:
            rawData = get_example_txt(f"zauberschuleSelf{x}.txt", EXAMPLES_PATH)
            print(f"Eigenes Beispiel {x+1}:")
        else:
            rawData = get_example_txt(f"zauberschule{x}.txt", EXAMPLES_PATH)
            print(f"Beispiel {x+1}:")

        # InputProcessing
        x, y = [int(data) for data in rawData[0].split()]

        floors = [
            np.array([list(line) for line in rawData[1 : x + 1]]),
            np.array([list(line) for line in rawData[x + 2 : 2 * x + 2]]),
        ]
        startPos = np.argwhere(floors[0] == "A")[0]
        endPos = np.argwhere(floors[0] == "B")[0]

        startNode: Node = Node((startPos[0], startPos[1], 0))
        endNode: Node = Node((endPos[0], endPos[1], 0))

        # run aStar
        path: list[tuple[int, int, int]] = a_star(startNode, endNode, floors)
        x: int
        y: int
        floor: int

        if not path:
            print("Kein Weg gefunden")
            exit(1)

        for index, (y, x, floor) in enumerate(path):
            if index == len(path) - 1:
                continue
            replace: chr = ""
            if floor != path[index + 1][2]:
                replace = "!"
            elif x - path[index + 1][1] == 1:
                replace = "<"
            elif x - path[index + 1][1] == -1:
                replace = ">"
            elif y - path[index + 1][0] == 1:
                replace = "^"
            elif y - path[index + 1][0] == -1:
                replace = "v"

            if replace != "":
                floors[floor][y][x] = replace

        for floor in floors:
            print(
                np.array2string(
                    floor,
                    separator="",
                    formatter={"str_kind": lambda x: x},
                    threshold=sys.maxsize,
                    max_line_width=sys.maxsize,
                )
            )

        print()


if __name__ == "__main__":
    main()
