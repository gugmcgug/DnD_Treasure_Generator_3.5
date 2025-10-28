"""Coin generation logic for treasure hoards."""

from typing import List

from dnd_treasure.core.dice import Dice
from dnd_treasure.core.models import TreasureType, CoinType


class CoinGenerator:
    """Generates coins based on treasure level and type."""

    def __init__(self, dice: Dice):
        """
        Initialize coin generator.

        Args:
            dice: Dice roller for random generation.
        """
        self.dice = dice

    def generate(
        self,
        level: int,
        treasure_type: TreasureType,
        percentage: float = 1.0
    ) -> List[str]:
        """
        Generate coins for a treasure hoard.

        Args:
            level: Encounter level (1-20).
            treasure_type: Type of treasure (NONE, STANDARD, DOUBLE, TRIPLE).
            percentage: Multiplier for coin amounts (default 1.0).

        Returns:
            List of coin strings (e.g., ["100 gp", "50 sp"]).
        """
        if treasure_type == TreasureType.NONE:
            return ["No Coins"]

        coins = []

        # Generate first set
        coin_str = self._generate_single(level, percentage)
        if coin_str != "No Coins":
            coins.append(coin_str)

        # Generate additional sets for double/triple
        if treasure_type == TreasureType.DOUBLE:
            coin_str = self._generate_single(level, percentage)
            if coin_str != "No Coins":
                coins.append(coin_str)
        elif treasure_type == TreasureType.TRIPLE:
            for _ in range(2):
                coin_str = self._generate_single(level, percentage)
                if coin_str != "No Coins":
                    coins.append(coin_str)

        return coins if coins else ["No Coins"]

    def _generate_single(self, level: int, percentage: float = 1.0) -> str:
        """
        Generate a single set of coins based on level.

        This implements the DMG treasure tables for coin generation.

        Args:
            level: Encounter level (1-20).
            percentage: Multiplier for coin amounts.

        Returns:
            Coin string (e.g., "100 gp") or "No Coins".
        """
        roll = self.dice.d100()
        value = 0
        coin_type = None

        # Implement DMG coin tables by level
        # This is a simplified version - full implementation would have all 20 levels
        if level == 1:
            if 1 <= roll <= 14:
                return "No Coins"
            elif 15 <= roll <= 29:
                value = self._roll_coins(1, 6, 1000)
                coin_type = "cp"
            elif 30 <= roll <= 52:
                value = self._roll_coins(1, 8, 100)
                coin_type = "sp"
            elif 53 <= roll <= 95:
                value = self._roll_coins(2, 8, 10)
                coin_type = "gp"
            else:  # 96-100
                value = self._roll_coins(1, 4, 10)
                coin_type = "pp"
        elif level <= 4:
            # Simplified - higher levels would have similar tables
            if 1 <= roll <= 10:
                return "No Coins"
            elif 11 <= roll <= 30:
                value = self._roll_coins(2, 10, 1000)
                coin_type = "cp"
            elif 31 <= roll <= 60:
                value = self._roll_coins(4, 8, 100)
                coin_type = "sp"
            elif 61 <= roll <= 95:
                value = self._roll_coins(4, 10, 10)
                coin_type = "gp"
            else:
                value = self._roll_coins(2, 8, 10)
                coin_type = "pp"
        else:
            # Higher levels (simplified)
            if 1 <= roll <= 10:
                return "No Coins"
            elif 11 <= roll <= 25:
                value = self._roll_coins(2, 10, 1000)
                coin_type = "sp"
            elif 26 <= roll <= 75:
                value = self._roll_coins(6, 4, 100)
                coin_type = "gp"
            else:
                value = self._roll_coins(5, 6, 10)
                coin_type = "pp"

        if value > 0 and coin_type:
            value = int(value * percentage)
            return f"{value} {coin_type}"

        return "No Coins"

    def _roll_coins(self, num_dice: int, die_size: int, multiplier: int) -> int:
        """
        Roll dice for coin generation.

        Args:
            num_dice: Number of dice to roll.
            die_size: Size of each die.
            multiplier: Multiply result by this value.

        Returns:
            Total coins rolled.
        """
        return self.dice.roll(die_size, num_dice) * multiplier
