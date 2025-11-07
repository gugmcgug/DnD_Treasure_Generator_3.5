"""Goods generation logic for treasure hoards (gems and art objects)."""

from typing import List

from dnd_treasure.core.dice import Dice
from dnd_treasure.core.models import TreasureType
from dnd_treasure.data.loader import ChartLoader


class GoodsGenerator:
    """Generates goods (gems and art objects) based on treasure level and type."""

    def __init__(self, dice: Dice, chart_loader: ChartLoader):
        """
        Initialize goods generator.

        Args:
            dice: Dice roller for random generation.
            chart_loader: Chart loader for accessing gem/art tables.
        """
        self.dice = dice
        self.chart_loader = chart_loader

    def generate(
        self,
        level: int,
        treasure_type: TreasureType,
        percentage: float = 1.0
    ) -> List[str]:
        """
        Generate goods for a treasure hoard.

        Args:
            level: Encounter level (1-20).
            treasure_type: Type of treasure (NONE, STANDARD, DOUBLE, TRIPLE).
            percentage: Multiplier for goods chances (default 1.0).

        Returns:
            List of goods strings (e.g., ["Ruby (5000 gp)", "Silver Ewer (60 gp)"]).
        """
        if treasure_type == TreasureType.NONE:
            return ["No Goods"]

        goods = []

        # Generate first set
        goods_list = self._generate_single(level, percentage)
        goods.extend(goods_list)

        # Generate additional sets for double/triple
        if treasure_type == TreasureType.DOUBLE:
            goods_list = self._generate_single(level, percentage)
            if goods_list and goods_list[0] != "No Goods":
                goods.extend(goods_list)
        elif treasure_type == TreasureType.TRIPLE:
            for _ in range(2):
                goods_list = self._generate_single(level, percentage)
                if goods_list and goods_list[0] != "No Goods":
                    goods.extend(goods_list)

        return goods if goods else ["No Goods"]

    def _generate_single(self, level: int, percentage: float = 1.0) -> List[str]:
        """
        Generate a single set of goods based on level.

        This implements the DMG treasure tables for goods generation.

        Args:
            level: Encounter level (1-20).
            percentage: Multiplier for goods chances.

        Returns:
            List of goods strings.
        """
        # Roll percentage chance
        if self.dice.d100() / 100 > percentage:
            return ["No Goods"]

        roll = self.dice.d100()
        goods = []

        # Implement DMG goods tables by level
        if level == 1:
            if roll >= 91 and roll <= 95:
                goods.append(self._generate_gem())
            elif roll >= 96 and roll <= 100:
                goods.append(self._generate_art())
        elif level == 2:
            if roll >= 82 and roll <= 95:
                for _ in range(self.dice.d3()):
                    goods.append(self._generate_gem())
            elif roll >= 96 and roll <= 100:
                for _ in range(self.dice.d3()):
                    goods.append(self._generate_art())
        elif level == 3:
            if roll >= 78 and roll <= 95:
                for _ in range(self.dice.d3()):
                    goods.append(self._generate_gem())
            elif roll >= 96 and roll <= 100:
                for _ in range(self.dice.d3()):
                    goods.append(self._generate_art())
        elif level == 4:
            if roll >= 71 and roll <= 95:
                for _ in range(self.dice.d4()):
                    goods.append(self._generate_gem())
            elif roll >= 96 and roll <= 100:
                for _ in range(self.dice.d3()):
                    goods.append(self._generate_art())
        elif level == 5:
            if roll >= 61 and roll <= 95:
                for _ in range(self.dice.d4()):
                    goods.append(self._generate_gem())
            elif roll >= 96 and roll <= 100:
                for _ in range(self.dice.d4()):
                    goods.append(self._generate_art())
        elif level == 6:
            if roll >= 57 and roll <= 92:
                for _ in range(self.dice.d4()):
                    goods.append(self._generate_gem())
            elif roll >= 93 and roll <= 100:
                for _ in range(self.dice.d4()):
                    goods.append(self._generate_art())
        elif level == 7:
            if roll >= 49 and roll <= 88:
                for _ in range(self.dice.d4()):
                    goods.append(self._generate_gem())
            elif roll >= 89 and roll <= 100:
                for _ in range(self.dice.d4()):
                    goods.append(self._generate_art())
        elif level == 8:
            if roll >= 46 and roll <= 85:
                for _ in range(self.dice.d6()):
                    goods.append(self._generate_gem())
            elif roll >= 86 and roll <= 100:
                for _ in range(self.dice.d4()):
                    goods.append(self._generate_art())
        elif level == 9:
            if roll >= 41 and roll <= 80:
                for _ in range(self.dice.d8()):
                    goods.append(self._generate_gem())
            elif roll >= 81 and roll <= 100:
                for _ in range(self.dice.d4()):
                    goods.append(self._generate_art())
        elif level == 10:
            if roll >= 36 and roll <= 79:
                for _ in range(self.dice.d8()):
                    goods.append(self._generate_gem())
            elif roll >= 80 and roll <= 100:
                for _ in range(self.dice.d6()):
                    goods.append(self._generate_art())
        elif level == 11:
            if roll >= 25 and roll <= 74:
                for _ in range(self.dice.d10()):
                    goods.append(self._generate_gem())
            elif roll >= 75 and roll <= 100:
                for _ in range(self.dice.d6()):
                    goods.append(self._generate_art())
        elif level == 12:
            if roll >= 18 and roll <= 70:
                for _ in range(self.dice.d10()):
                    goods.append(self._generate_gem())
            elif roll >= 71 and roll <= 100:
                for _ in range(self.dice.d8()):
                    goods.append(self._generate_art())
        elif level == 13:
            if roll >= 12 and roll <= 66:
                for _ in range(self.dice.d12()):
                    goods.append(self._generate_gem())
            elif roll >= 67 and roll <= 100:
                for _ in range(self.dice.d10()):
                    goods.append(self._generate_art())
        elif level == 14:
            if roll >= 12 and roll <= 66:
                for _ in range(self.dice.d8(2)):  # 2d8
                    goods.append(self._generate_gem())
            elif roll >= 67 and roll <= 100:
                for _ in range(self.dice.d6(2)):  # 2d6
                    goods.append(self._generate_art())
        elif level == 15:
            if roll >= 10 and roll <= 65:
                for _ in range(self.dice.d10(2)):  # 2d10
                    goods.append(self._generate_gem())
            elif roll >= 66 and roll <= 100:
                for _ in range(self.dice.d8(2)):  # 2d8
                    goods.append(self._generate_art())
        elif level == 16:
            if roll >= 8 and roll <= 64:
                for _ in range(self.dice.d6(4)):  # 4d6
                    goods.append(self._generate_gem())
            elif roll >= 65 and roll <= 100:
                for _ in range(self.dice.d10(2)):  # 2d10
                    goods.append(self._generate_art())
        elif level == 17:
            if roll >= 5 and roll <= 63:
                for _ in range(self.dice.d8(4)):  # 4d8
                    goods.append(self._generate_gem())
            elif roll >= 64 and roll <= 100:
                for _ in range(self.dice.d8(3)):  # 3d8
                    goods.append(self._generate_art())
        elif level == 18:
            if roll >= 5 and roll <= 54:
                for _ in range(self.dice.d12(3)):  # 3d12
                    goods.append(self._generate_gem())
            elif roll >= 55 and roll <= 100:
                for _ in range(self.dice.d10(3)):  # 3d10
                    goods.append(self._generate_art())
        elif level == 19:
            if roll >= 4 and roll <= 50:
                for _ in range(self.dice.d6(6)):  # 6d6
                    goods.append(self._generate_gem())
            elif roll >= 51 and roll <= 100:
                for _ in range(self.dice.d6(6)):  # 6d6
                    goods.append(self._generate_art())
        elif level == 20:
            if roll >= 3 and roll <= 38:
                for _ in range(self.dice.d10(4)):  # 4d10
                    goods.append(self._generate_gem())
            elif roll >= 39 and roll <= 100:
                for _ in range(self.dice.d6(7)):  # 7d6
                    goods.append(self._generate_art())

        return goods if goods else ["No Goods"]

    def _generate_gem(self) -> str:
        """Generate a single gem."""
        # Roll for gem tier
        roll = self.dice.d100()

        if roll <= 25:
            tier = 1
        elif roll <= 50:
            tier = 2
        elif roll <= 70:
            tier = 3
        elif roll <= 90:
            tier = 4
        elif roll <= 99:
            tier = 5
        else:  # 100
            tier = 6

        # Load appropriate gem chart
        chart = self.chart_loader.load_chart_by_name(f"dmg/gems_tier{tier}")

        # Roll on chart
        die_size = int(chart.roll_die[1:]) if chart.roll_die.startswith('d') else 100
        gem_roll = self.dice.roll(die_size)
        entry = chart.find_entry(gem_roll)

        if entry:
            # Calculate gem value based on tier
            value = self._calculate_gem_value(tier)
            return f"{entry.name} ({value} gp)"

        return "Unknown Gem (10 gp)"

    def _generate_art(self) -> str:
        """Generate a single art object."""
        # Roll for art tier
        roll = self.dice.d100()

        if roll <= 10:
            tier = 1
        elif roll <= 25:
            tier = 2
        elif roll <= 40:
            tier = 3
        elif roll <= 50:
            tier = 4
        elif roll <= 60:
            tier = 5
        elif roll <= 70:
            tier = 6
        elif roll <= 80:
            tier = 7
        elif roll <= 85:
            tier = 8
        elif roll <= 90:
            tier = 9
        elif roll <= 95:
            tier = 10
        elif roll <= 99:
            tier = 11
        else:  # 100
            tier = 12

        # Load appropriate art chart
        chart = self.chart_loader.load_chart_by_name(f"dmg/art_tier{tier}")

        # Roll on chart
        die_size = int(chart.roll_die[1:]) if chart.roll_die.startswith('d') else 10
        art_roll = self.dice.roll(die_size)
        entry = chart.find_entry(art_roll)

        if entry:
            # Calculate art value based on tier
            value = self._calculate_art_value(tier)
            return f"{entry.name} ({value} gp)"

        return "Unknown Art Object (50 gp)"

    def _calculate_gem_value(self, tier: int) -> int:
        """Calculate gem value based on tier using DMG formulas."""
        if tier == 1:
            return self.dice.d4(4)  # 4d4 gp
        elif tier == 2:
            return self.dice.d4(2) * 10  # 2d4 × 10 gp
        elif tier == 3:
            return self.dice.d4(4) * 10  # 4d4 × 10 gp
        elif tier == 4:
            return self.dice.d4(2) * 100  # 2d4 × 100 gp
        elif tier == 5:
            return self.dice.d4(4) * 100  # 4d4 × 100 gp
        elif tier == 6:
            return self.dice.d4(2) * 1000  # 2d4 × 1000 gp
        return 10

    def _calculate_art_value(self, tier: int) -> int:
        """Calculate art object value based on tier using DMG formulas."""
        if tier == 1:
            return self.dice.d10() * 10  # 1d10 × 10 gp
        elif tier == 2:
            return self.dice.d6(3) * 10  # 3d6 × 10 gp
        elif tier == 3:
            return self.dice.d6() * 100  # 1d6 × 100 gp
        elif tier == 4:
            return self.dice.d10() * 100  # 1d10 × 100 gp
        elif tier == 5:
            return self.dice.d6(2) * 100  # 2d6 × 100 gp
        elif tier == 6:
            return self.dice.d6(3) * 100  # 3d6 × 100 gp
        elif tier == 7:
            return self.dice.d6(4) * 100  # 4d6 × 100 gp
        elif tier == 8:
            return self.dice.d6(5) * 100  # 5d6 × 100 gp
        elif tier == 9:
            return self.dice.d4() * 1000  # 1d4 × 1000 gp
        elif tier == 10:
            return self.dice.d6() * 1000  # 1d6 × 1000 gp
        elif tier == 11:
            return self.dice.d4(2) * 1000  # 2d4 × 1000 gp
        elif tier == 12:
            return self.dice.d6(2) * 1000  # 2d6 × 1000 gp
        return 50
