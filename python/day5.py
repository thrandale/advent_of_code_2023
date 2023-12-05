from solution import Solution


class Day5(Solution):
    @classmethod
    def _Part1(cls) -> int:
        seeds = [
            [seed]
            for seed in map(int, cls.inputBlocks[0].split(": ")[1].strip().split())
        ]
        almanac = [
            [list(map(int, a.split())) for a in b.split("\n")[1:]]
            for b in cls.inputBlocks[1:]
        ]

        for i in range(len(seeds)):
            for j, mapping in enumerate(almanac):
                for dest, source, length in mapping:
                    value = seeds[i][j]
                    if value < source or value > source + length:
                        continue

                    seeds[i].append(dest + (value - source))
                    break
                else:
                    seeds[i].append(seeds[i][j])

        return min(seeds, key=lambda x: x[-1])[-1]

    @classmethod
    def _Part2(cls) -> int:
        return 0


Day5.Run("day5.txt")
