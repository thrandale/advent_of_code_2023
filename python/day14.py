from solution import Solution


class Day14(Solution):
    @classmethod
    def _Part1(cls) -> int:
        grid = list(map(list, zip(*cls.inputLines)))
        counts = [0 for _ in range(len(grid))]

        for line in grid:
            empty = rocks = 0
            for i, c in enumerate(line):
                if c == ".":
                    empty += 1
                elif c == "O":
                    rocks += 1
                elif c == "#":
                    for j in range(i - empty - rocks, i - empty):
                        counts[j] += 1

                    empty = rocks = 0

            for j in range(len(line) - empty - rocks, len(line) - empty):
                counts[j] += 1

        return sum((len(line) - i) * c for i, c in enumerate(counts))

    @classmethod
    def _Part2(cls) -> int:
        total = 0

        return total


Day14.Run("day14.txt")
