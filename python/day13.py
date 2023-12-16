import re

from solution import Solution


class day13(Solution):
    HLINE_REGEX = re.compile(r"([#.].*\n)\1")

    @staticmethod
    def GetLinesAboveMirror(cls, block: str) -> int:
        lineLength = block.index("\n") + 1
        match = cls.HLINE_REGEX.search(block)
        if match is None:
            return 0

        middle = match.start() + lineLength
        if middle > len(block) / 2:
            secondHalf = block[middle:].strip()
            firstHalf = block[middle - len(secondHalf) - 1 : middle].strip()
        else:
            firstHalf = block[:middle].strip()
            secondHalf = block[len(firstHalf) : len(firstHalf) * 2].strip()

        # Reverse the order of the lines in the second half
        secondHalf = "\n".join(secondHalf.split("\n")[::-1]).strip()
        rowsAbove = match.start() // lineLength + 1
        if firstHalf == secondHalf:
            return rowsAbove
        else:
            return 0

    @classmethod
    def _Part1(cls) -> int:
        colsToLeft = 0
        colsAbove = 0
        for block in cls.inputBlocks:
            colsAbove += cls.GetLinesAboveMirror(cls, block)
            inverted = "\n".join(map(lambda c: "".join(c), zip(*block.split("\n"))))
            colsToLeft += cls.GetLinesAboveMirror(cls, inverted)

        return colsToLeft + colsAbove * 100

    @classmethod
    def _Part2(cls) -> int:
        total = 0

        return total


day13.Run("day13test.txt")
