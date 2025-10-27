"""Dice rolling utilities for D&D treasure generation."""

import random
from typing import Optional


class Dice:
    """Handles all dice rolling operations."""

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize dice roller.

        Args:
            seed: Optional random seed for reproducible results in tests.
        """
        self._random = random.Random(seed)

    def roll(self, num_sides: int, num_dice: int = 1) -> int:
        """
        Roll dice and return the sum.

        Args:
            num_sides: Number of sides on each die.
            num_dice: Number of dice to roll (default 1).

        Returns:
            Sum of all dice rolled.
        """
        return sum(self._random.randint(1, num_sides) for _ in range(num_dice))

    def d100(self, num_dice: int = 1) -> int:
        """Roll d100 (1-100)."""
        return self.roll(100, num_dice)

    def d20(self, num_dice: int = 1) -> int:
        """Roll d20 (1-20)."""
        return self.roll(20, num_dice)

    def d12(self, num_dice: int = 1) -> int:
        """Roll d12 (1-12)."""
        return self.roll(12, num_dice)

    def d10(self, num_dice: int = 1) -> int:
        """Roll d10 (1-10)."""
        return self.roll(10, num_dice)

    def d8(self, num_dice: int = 1) -> int:
        """Roll d8 (1-8)."""
        return self.roll(8, num_dice)

    def d6(self, num_dice: int = 1) -> int:
        """Roll d6 (1-6)."""
        return self.roll(6, num_dice)

    def d4(self, num_dice: int = 1) -> int:
        """Roll d4 (1-4)."""
        return self.roll(4, num_dice)

    def d3(self, num_dice: int = 1) -> int:
        """Roll d3 (1-3)."""
        return self.roll(3, num_dice)

    def d2(self, num_dice: int = 1) -> int:
        """Roll d2 (1-2)."""
        return self.roll(2, num_dice)
