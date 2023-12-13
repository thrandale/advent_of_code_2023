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

    @staticmethod
    def IsInGrid(grid: list[list[str]], coords: tuple[int, int]) -> bool:
        return 0 <= coords[0] < len(grid[0]) and 0 <= coords[1] < len(grid)

    @classmethod
    def GetFirstMove(
        cls, grid: list[list[str]]
    ) -> tuple[tuple[int, int], int, str, tuple[int, int]]:
        sIndex = "".join(cls.inputLines).index("S")
        sPos = (sIndex % len(grid[0]), sIndex // len(grid[0]))
        for d in Dir:
            coords = cls.CoordsForDir(sPos, d)
            char = grid[coords[1]][coords[0]]
            if (d + 2) % 4 in cls.VALID_DIRS[char]:
                return (sPos, (d + 2) % 4, char, coords)

    @staticmethod
    def DrawGrid(
        grid: list[list[str]],
        pathNodes: set[tuple[int, int]],
        notEnclosed: set[tuple[int, int]],
    ):
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if (x, y) in pathNodes:
                    print(colored(grid[y][x], "blue"), end="")
                elif (x, y) in notEnclosed:
                    print(colored("O", "red"), end="")
                else:
                    print(colored("I", "green"), end="")
            print()

    @classmethod
    def _Part1(cls) -> int:
        steps = 1  # Start node is already a step
        grid = cls.GetGrid()
        sPos, lastDir, currentChar, currentPos = cls.GetFirstMove(grid)

        while True:
            nextDir = cls.VALID_DIRS[currentChar].difference({lastDir}).pop()
            currentPos = cls.CoordsForDir(currentPos, nextDir)
            if currentPos == sPos:
                steps += 1
                break

            currentChar = grid[currentPos[1]][currentPos[0]]
            lastDir = (nextDir + 2) % 4
            steps += 1

        return int(steps / 2)

    @staticmethod
    def UpdateNodeGroup(
        grid: list[list[str]],
        node: tuple[int, int],
        pathNodes: set[tuple[int, int]],
        group: set[tuple[int, int]] = set(),
    ) -> set[tuple[int, int]]:
        """Recursively gets all the nodes that are connected to the given node
        excluding the nodes in the pathNodes set"""
        if node in pathNodes:
            return

        group.add(node)
        allChecked = True
        for d in Dir:
            coords = Day10.CoordsForDir(node, d)
            if (
                not Day10.IsInGrid(grid, coords)
                or coords in group
                or coords in pathNodes
            ):
                continue

            allChecked = False
            Day10.UpdateNodeGroup(grid, coords, pathNodes, group)

        if allChecked:
            return

    @classmethod
    def _Part2(cls) -> int:
        cornerDirs = {
            "L": {Dir.DOWN, Dir.LEFT},
            "F": {Dir.LEFT, Dir.UP},
            "7": {Dir.UP, Dir.RIGHT},
            "J": {Dir.RIGHT, Dir.DOWN},
        }

        grid = cls.GetGrid()
        width, height = len(grid[0]), len(grid)
        sPos, lastDir, currentChar, currentPos = cls.GetFirstMove(grid)

        topDir = {(lastDir - 1) % 4}
        prevTopDir = topDir
        pathNodes = {sPos}
        top = set()
        bottom = set()

        while True:
            pathNodes.add(currentPos)
            nextDir = cls.VALID_DIRS[currentChar].difference({lastDir}).pop()

            # If this is a corner, there is two possible top directions
            if currentChar in cornerDirs:
                prevTopDir = topDir.pop()
                topDir = cornerDirs[currentChar].copy()
                if (lastDir - 1) % 4 not in topDir:
                    # Rotation needs to be reversed
                    topDir = {(d + 2) % 4 for d in topDir}

            # Add the adjacent nodes to the top or bottom
            for d in Dir:
                if d == lastDir or d == nextDir:
                    continue

                coords = cls.CoordsForDir(currentPos, d)

                if not cls.IsInGrid(grid, coords):
                    continue

                if d in topDir:
                    top.add(coords)
                elif (d + 2) % 4 in topDir:
                    bottom.add(coords)

            currentPos = cls.CoordsForDir(currentPos, nextDir)
            if currentPos == sPos:
                break

            # If this was a corner, remove the previous top direction
            if len(topDir) == 2:
                topDir.remove(prevTopDir)

            lastDir = (nextDir + 2) % 4
            currentChar = grid[currentPos[1]][currentPos[0]]

        # Get all the nodes that are not enclosed by the path
        notEnclosed = set()
        nodesOnEdge = {(i, j) for i in range(width) for j in [0, height - 1]} | {
            (i, j) for j in range(height) for i in [0, width - 1]
        }
        for node in nodesOnEdge:
            Day10.UpdateNodeGroup(grid, node, pathNodes, notEnclosed)

        # Add either the top or bottom nodes to the notEnclosed set
        # depending on which one is outside the enclosed area
        if bottom.intersection(notEnclosed):
            for node in bottom.difference(notEnclosed):
                Day10.UpdateNodeGroup(grid, node, pathNodes, notEnclosed)
        elif top.intersection(notEnclosed):
            for node in top.difference(notEnclosed):
                Day10.UpdateNodeGroup(grid, node, pathNodes, notEnclosed)

        # cls.DrawGrid(grid, pathNodes, notEnclosed)

        return width * height - len(pathNodes) - len(notEnclosed)


Day10.Run("day10.txt")
