import os

from contextlib import contextmanager
from time import time


class Solution:
    def __init__(self, inputFile):
        inputFile = os.path.join(os.getcwd(), "input", inputFile)
        with open(inputFile, "r") as f:
            self.input: str = f.read().strip()

    @contextmanager
    def __TimeRun(self):
        start = time()
        yield
        end = time()
        total = end - start
        if total < 0.001:
            print(f"Took {total * 1000:.6f}ms")
        else:
            print(f"Took {total:.3f}s")

    def _GetInputLines(self) -> list[str]:
        return self.input.split("\n")

    def _GetInputBlocks(self) -> list[str]:
        return self.input.split("\n\n")

    def _Part1(self) -> int:
        raise NotImplementedError

    def _Part2(self) -> int:
        raise NotImplementedError

    def Part1(self) -> int:
        with self.__TimeRun():
            result = self._Part1()
            print(f"Part 1: {result}", end=", ")

    def Part2(self) -> int:
        with self.__TimeRun():
            result = self._Part2()
            print(f"Part 2: {result}", end=", ")
