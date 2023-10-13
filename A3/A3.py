import heapq
import numpy as np

OWNEXAMPLES = False


# utility
def getExampleTxt(path: str) -> list[str]:
    """ließt das Beispiel am relativen Pfand ein

    :param path: Der relative pfad von der txt-Datei des Beispiels
    :returns: eine liste von Zeilen des Beispiels
    """
    return [line.strip() for line in open(path).readlines()]


# A*
class Node:
    """Eine einfache Node Klasse für backtracking und Cost berechnen, speichert auch die Position"""

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
        return hash(self.position) + hash(self.parent.position) if self.parent else 0


def heuristicCost(nodePos: tuple[int, int, int], goalPos: tuple[int, int, int]) -> int:
    x1, y1, f1 = nodePos
    x2, y2, f2 = goalPos

    return (
        abs(x1 - x2) + abs(y1 - y2) + abs(f1 - f2) * 3
    )  # idk if we should consider floor cost


def getNeighbors(node, floors, goalPos: tuple[int, int, int]):
    x, y, f = node.position
    neighbors = []

    for ajacentX, ajacentY in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        newX, newY = x + ajacentX, y + ajacentY
        if floors[f][newX][newY] != "#":
            neighbors.append(
                Node(
                    (newX, newY, f),
                    parent=node,
                    cost=node.cost + 1 + heuristicCost((newX, newY, f), goalPos),
                )
            )

    if floors[1 - f][x][y] != "#":
        neighbors.append(
            Node(
                (x, y, 1 - f),
                parent=node,
                cost=node.cost + 3 + heuristicCost((x, y, 1 - f), goalPos),
            )
        )  # for two floor 1-f because 0->1 and 1->0

    return neighbors


def aStar(start: Node, goal: Node, floors) -> list[tuple[int, int, int]]:
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

        for neighbor in getNeighbors(curNode, floors, goal.position):
            if neighbor in explored:
                # already seen dont care
                continue

            if neighbor not in queque:
                heapq.heappush(queque, neighbor)


def main():
    for x in range(1):
        if OWNEXAMPLES:
            rawData = getExampleTxt(f"zauberschuleSelf{x}.txt")
            print(f"Eigenes Beispiel {x+1}:")
        else:
            rawData = getExampleTxt(f"zauberschule{x}.txt")
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
        #visualize

        #run aStar
        path: list[tuple[int, int, int]] = aStar(startNode, endNode, floors)
        x: int
        y: int
        floor: int
        for index, (y, x, floor) in enumerate(path):
            if index == len(path) - 1:
                continue
            replace: chr = ""
            if floor != path[index + 1][2]:
                replace = "!"
                print(x, y)
                print(path[index + 1][0])
            elif x - path[index + 1][1] == 1:
                replace = "<"
            elif x - path[index + 1][1] == -1:
                replace = ">"
            elif y - path[index + 1][0] == 1:
                replace = "v"
            elif y - path[index + 1][0] == -1:
                replace = "^"

            if replace != "":
                floors[floor][y][x] = replace

        for floor in floors:
            print(np.array2string(floor,separator="",formatter={'str_kind': lambda x: x}))

        print()


if __name__ == "__main__":
    main()
