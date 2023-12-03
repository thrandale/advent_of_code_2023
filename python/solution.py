import os

from contextlib import contextmanager
from time import time


class Solution:
    inputBlocks: list[str]
    inputLines: list[str]
    inputText: str

    @classmethod
    def __Part1(cls) -> int:
        with cls.__TimeIt():
            result = cls._Part1()
            print(f"Part 1: {result}", end=", ")

    @classmethod
    def __Part2(cls) -> int:
        with cls.__TimeIt():
            result = cls._Part2()
            print(f"Part 2: {result}", end=", ")

    @staticmethod
    @contextmanager
    def __TimeIt() -> None:
        start = time()
        yield
        end = time()
        total = end - start
        if total < 0.01:
            print(f"Took {total * 1000:.4f}ms")
        else:
            print(f"Took {total:.3f}s")

    @classmethod
    def _Part1(cls) -> int:
        raise NotImplementedError

    @classmethod
    def _Part2(cls) -> int:
        raise NotImplementedError

    @classmethod
    def Run(cls, inputFile: str) -> None:
        inputFile = os.path.join(os.getcwd(), "input", inputFile)

        with open(inputFile, "r") as f:
            cls.inputText = f.read().strip()

        cls.inputBlocks = cls.inputText.split("\n\n")
        cls.inputLines = cls.inputText.split("\n")

        cls.__Part1()
        cls.__Part2()
