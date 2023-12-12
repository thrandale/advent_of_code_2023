from enum import Enum
from solution import Solution


class Dir(int, Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Day10(Solution):
    @staticmethod
    def CoordsForDir(current: tuple[int, int], direction: Dir) -> tuple[int, int]:
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
        validDirs = {
            "|": {Dir.UP, Dir.DOWN},
            "-": {Dir.RIGHT, Dir.LEFT},
            "L": {Dir.UP, Dir.RIGHT},
            "J": {Dir.UP, Dir.LEFT},
            "7": {Dir.DOWN, Dir.LEFT},
            "F": {Dir.RIGHT, Dir.DOWN},
        }

        steps = 1
        sIndex = "".join(cls.inputLines).index("S")
        grid = [list(line) for line in cls.inputLines]
        sPos = (sIndex % len(grid[0]), sIndex // len(grid[0]))

        for d in Dir:
            coords = cls.CoordsForDir(sPos, d)
            char = grid[coords[1]][coords[0]]
            if (d + 2) % 4 in validDirs[char]:
                lastDir = {d}
                currentChar = char
                currentPos = coords
                break

        while True:
            nextDir = validDirs[currentChar].difference(lastDir).pop()
            nextCoords = cls.CoordsForDir(currentPos, nextDir)
            nextChar = grid[nextCoords[1]][nextCoords[0]]
            if nextChar == "S":
                steps += 1
                break

            currentChar = nextChar
            lastDir = {(nextDir + 2) % 4}
            currentPos = nextCoords
            steps += 1

        return int(steps / 2)

    @classmethod
    def _Part2(cls) -> int:
        total = 0

        return total


Day10.Run("day10.txt")
