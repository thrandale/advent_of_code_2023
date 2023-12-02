from solution import Solution


class Day2(Solution):
    @classmethod
    def _Part1(cls) -> int:
        total = 0
        maxColors = {"red": 12, "green": 13, "blue": 14}

        for i, game in enumerate(cls.inputLines):
            if any(
                int(count) > maxColors[color]
                for count, color in [
                    s.strip().split(" ")
                    for r in game[game.find(":") + 2 :].split(";")
                    for s in r.split(",")
                ]
            ):
                continue

            total += i + 1

        return total

    @classmethod
    def _Part2(cls) -> int:
        total = 0
        for game in cls.inputLines:
            minColor = {"red": 0, "green": 0, "blue": 0}
            for r in game[game.find(":") + 2 :].split(";"):
                for s in r.split(","):
                    count, color = s.strip().split(" ")
                    minColor[color] = max(minColor[color], int(count))

            total += minColor["red"] * minColor["green"] * minColor["blue"]

        return total


Day2.Run("day2.txt")
