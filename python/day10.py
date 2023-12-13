import sys

from enum import Enum
from solution import Solution
from termcolor import colored


sys.setrecursionlimit(10000)


class Dir(int, Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Day10(Solution):
    VALID_DIRS = {
        "|": {Dir.UP, Dir.DOWN},
        "-": {Dir.RIGHT, Dir.LEFT},
        "L": {Dir.UP, Dir.RIGHT},
        "J": {Dir.UP, Dir.LEFT},
        "7": {Dir.DOWN, Dir.LEFT},
        "F": {Dir.RIGHT, Dir.DOWN},
        ".": {},
    }

    @classmethod
    def GetGrid(cls) -> list[list[str]]:
        return [list(line) for line in cls.inputLines]

    @staticmethod
    def CoordsForDir(current: tuple[int, int], direction: Dir) -> tuple[int, int]:
        """Returns the coordinates of the next node in the given direction"""
        match direction:
            case Dir.UP:
                return (current[0], current[1] - 1)
            case Dir.RIGHT:
                return (current[0] + 1, current[1])
            case Dir.DOWN:
                return (current[0], current[1] + 1)
            case Dir.LEFT:
                return (current[0] - 1, current[1])

    @classmethod
    def _Part1(cls) -> int:
        steps = 1  # Start node is already a step
        grid = cls.GetGrid()
        sIndex = "".join(cls.inputLines).index("S")
        sPos = (sIndex % len(grid[0]), sIndex // len(grid[0]))
        for d in Dir:
            coords = cls.CoordsForDir(sPos, d)
            char = grid[coords[1]][coords[0]]
            if (d + 2) % 4 in cls.VALID_DIRS[char]:
                lastDir = (d + 2) % 4
                currentChar = char
                currentPos = coords
                break

        while True:
            nextDir = cls.VALID_DIRS[currentChar].difference({lastDir}).pop()
            currentPos = cls.CoordsForDir(currentPos, nextDir)
            currentChar = grid[currentPos[1]][currentPos[0]]
            if currentChar == "S":
                steps += 1
                break

            lastDir = (nextDir + 2) % 4
            steps += 1

        return int(steps / 2)

    @staticmethod
    def GetNodeGroup(
        grid: list[list[str]],
        node: tuple[int, int],
        pathNodes: set[tuple[int, int]],
        group: set[tuple[int, int]] = set(),
    ) -> set[tuple[int, int]]:
        """Recursively gets all the nodes that are connected to the given node
        excluding the nodes in the pathNodes set"""
        group.add(node)
        allChecked = True
        for d in Dir:
            coords = Day10.CoordsForDir(node, d)
            if (
                (
                    coords[0] < 0
                    or coords[1] < 0
                    or coords[0] >= len(grid[0])
                    or coords[1] >= len(grid)
                )
                or coords in group
                or coords in pathNodes
            ):
                continue

            allChecked = False
            Day10.GetNodeGroup(grid, coords, pathNodes, group)

        if allChecked:
            return group

        return group

    @classmethod
    def _Part2(cls) -> int:
        cornerDirs = {
            "L": {Dir.DOWN, Dir.LEFT},
            "F": {Dir.LEFT, Dir.UP},
            "7": {Dir.UP, Dir.RIGHT},
            "J": {Dir.RIGHT, Dir.DOWN},
        }

        grid = cls.GetGrid()
        sIndex = "".join(cls.inputLines).index("S")
        startPos = (sIndex % len(grid[0]), sIndex // len(grid[0]))
        validDirsForStart = set()
        for d in Dir:
            coords = cls.CoordsForDir(startPos, d)
            char = grid[coords[1]][coords[0]]
            if (d + 2) % 4 in cls.VALID_DIRS[char]:
                lastDir = (d + 2) % 4
                currentChar = char
                currentPos = coords
                validDirsForStart.add(d)
            else:
                topDir = {d}

        # Replace the S with a valid char
        for key, value in cls.VALID_DIRS.items():
            if value == validDirsForStart:
                grid[startPos[1]][startPos[0]] = key
                break

        # for each node, the adjacent nodes that are adjacent to the path
        # {(x, y): {(x, y),...}}
        adjMap = {}
        pathNodes = {startPos}
        top = set()
        bottom = set()
        prevTopDir = topDir

        while True:
            adjMap.pop(currentPos, None)
            pathNodes.add(currentPos)
            nextDir = cls.VALID_DIRS[currentChar].difference({lastDir}).pop()
            # print()
            # print("TopDir:", topDir)
            # print("NextDir:", nextDir)
            # print("CurrentPos:", currentPos)
            # print("CurrentChar:", currentChar)

            # If this is a corner we need to update the topDir
            if currentChar in cornerDirs:
                # print("  Corner")
                prevTopDir = topDir.pop()
                topDir = cornerDirs[currentChar].copy()
                if (lastDir - 1) % 4 not in topDir:
                    # Reverse the order of the topDir
                    topDir = {(d + 2) % 4 for d in topDir}
                # print("  New topDir:", topDir)

            for d in Dir:
                if d == lastDir or d == nextDir:
                    continue

                coords = cls.CoordsForDir(currentPos, d)
                adjMap.setdefault(coords, set()).add(currentPos)

                if d in topDir:
                    top.add(coords)
                elif (d + 2) % 4 in topDir:
                    bottom.add(coords)

            currentPos = cls.CoordsForDir(currentPos, nextDir)
            if currentPos == startPos:
                break

            if len(topDir) == 2:
                topDir.remove(prevTopDir)
                # print("  After removal:", topDir)

            lastDir = (nextDir + 2) % 4
            currentChar = grid[currentPos[1]][currentPos[0]]

        notEnclosed = set()
        enclosed = set()

        # Check all the nodes along the edge
        width, height = len(grid[0]), len(grid)
        nodesOnEdge = {(i, j) for i in range(width) for j in [0, height - 1]} | {
            (i, j) for j in range(height) for i in [0, width - 1]
        }

        for node in nodesOnEdge:
            if node in pathNodes or node in notEnclosed:
                continue
            notEnclosed.update(Day10.GetNodeGroup(grid, node, pathNodes))

        if len(top.intersection(notEnclosed)) > 0:
            for node in top.difference(pathNodes):
                notEnclosed.update(
                    Day10.GetNodeGroup(grid, node, pathNodes, notEnclosed)
                )

        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if (x, y) in pathNodes:
                    print(colored(grid[y][x], "blue"), end="")
                # elif (x, y) in top:
                #     print(colored("T", "yellow"), end="")
                # elif (x, y) in bottom:
                #     print(colored("B", "yellow"), end="")
                # else:
                #     print(grid[y][x], end="")
                elif (x, y) in notEnclosed:
                    print(colored("O", "red"), end="")
                else:
                    enclosed.add((x, y))
                    print(colored("I", "green"), end="")
            print()

        return len(enclosed)


Day10.Run("day10test.txt")
