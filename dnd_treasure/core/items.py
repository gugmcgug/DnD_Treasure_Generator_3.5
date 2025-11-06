"""Magic item generation logic for treasure hoards."""

from typing import List

from dnd_treasure.core.dice import Dice
from dnd_treasure.core.keywords import KeywordReplacer
from dnd_treasure.core.models import Item, TreasureType, ItemPower
from dnd_treasure.data.loader import ChartLoader


class ItemGenerator:
    """Generates magic items based on treasure level and type."""

    def __init__(self, dice: Dice, chart_loader: ChartLoader, keyword_replacer: KeywordReplacer):
        """
        Initialize item generator.

        Args:
            dice: Dice roller for random generation.
            chart_loader: Chart loader for accessing item tables.
            keyword_replacer: Keyword replacer for dynamic item names.
        """
        self.dice = dice
        self.chart_loader = chart_loader
        self.keyword_replacer = keyword_replacer

    def generate(
        self,
        level: int,
        treasure_type: TreasureType,
        percentage: float = 1.0
    ) -> List[Item]:
        """
        Generate magic items for a treasure hoard.

        Args:
            level: Encounter level (1-20).
            treasure_type: Type of treasure (NONE, STANDARD, DOUBLE, TRIPLE).
            percentage: Multiplier for item chances (default 1.0).

        Returns:
            List of Item objects.
        """
        if treasure_type == TreasureType.NONE:
            return [Item(name="No Items", value=0, item_type="none")]

        items = []

        # Generate first set
        item_list = self._generate_single(level, percentage)
        items.extend(item_list)

        # Generate additional sets for double/triple
        if treasure_type == TreasureType.DOUBLE:
            item_list = self._generate_single(level, percentage)
            if item_list and item_list[0].name != "No Items":
                items.extend(item_list)
        elif treasure_type == TreasureType.TRIPLE:
            for _ in range(2):
                item_list = self._generate_single(level, percentage)
                if item_list and item_list[0].name != "No Items":
                    items.extend(item_list)

        return items if items else [Item(name="No Items", value=0, item_type="none")]

    def _generate_single(self, level: int, percentage: float = 1.0) -> List[Item]:
        """
        Generate a single set of items based on level.

        This implements the DMG treasure tables for item generation.

        Args:
            level: Encounter level (1-20).
            percentage: Multiplier for item chances.

        Returns:
            List of Items.
        """
        # Roll percentage chance
        if self.dice.d100() / 100 > percentage:
            return [Item(name="No Items", value=0, item_type="none")]

        roll = self.dice.d100()
        items = []

        # Implement DMG item tables by level (simplified from VB code)
        if level == 1:
            if roll <= 71:
                return [Item(name="No Items", value=0, item_type="none")]
            elif roll <= 95:
                # Mundane item
                items.append(self._generate_mundane())
            else:  # 96-100
                # Minor magic
                items.append(self._generate_minor_magic())
        elif level == 2:
            if roll <= 49:
                return [Item(name="No Items", value=0, item_type="none")]
            elif roll <= 85:
                items.append(self._generate_mundane())
            else:  # 86-100
                items.append(self._generate_minor_magic())
        elif level == 3:
            if roll <= 49:
                return [Item(name="No Items", value=0, item_type="none")]
            elif roll <= 79:
                # 1d3 mundane items
                for _ in range(self.dice.d3()):
                    items.append(self._generate_mundane())
            else:  # 80-100
                items.append(self._generate_minor_magic())
        elif level == 4:
            if roll <= 42:
                return [Item(name="No Items", value=0, item_type="none")]
            elif roll <= 62:
                for _ in range(self.dice.d4()):
                    items.append(self._generate_mundane())
            else:  # 63-100
                items.append(self._generate_minor_magic())
        elif level == 5:
            if roll <= 57:
                return [Item(name="No Items", value=0, item_type="none")]
            elif roll <= 67:
                for _ in range(self.dice.d4()):
                    items.append(self._generate_mundane())
            else:  # 68-100
                for _ in range(self.dice.d3()):
                    items.append(self._generate_minor_magic())
        elif level == 6:
            if roll <= 54:
                return [Item(name="No Items", value=0, item_type="none")]
            elif roll <= 59:
                for _ in range(self.dice.d4()):
                    items.append(self._generate_mundane())
            elif roll <= 99:
                for _ in range(self.dice.d3()):
                    items.append(self._generate_minor_magic())
            else:  # 100
                items.append(self._generate_medium_magic())
        elif level == 7:
            if roll <= 51:
                return [Item(name="No Items", value=0, item_type="none")]
            elif roll <= 97:
                for _ in range(self.dice.d3()):
                    items.append(self._generate_minor_magic())
            else:  # 98-100
                items.append(self._generate_medium_magic())
        elif level == 8:
            if roll <= 48:
                return [Item(name="No Items", value=0, item_type="none")]
            elif roll <= 96:
                for _ in range(self.dice.d4()):
                    items.append(self._generate_minor_magic())
            else:  # 97-100
                items.append(self._generate_medium_magic())
        elif level == 9:
            if roll <= 43:
                return [Item(name="No Items", value=0, item_type="none")]
            elif roll <= 91:
                for _ in range(self.dice.d4()):
                    items.append(self._generate_minor_magic())
            else:  # 92-100
                items.append(self._generate_medium_magic())
        elif level == 10:
            if roll <= 40:
                return [Item(name="No Items", value=0, item_type="none")]
            elif roll <= 88:
                for _ in range(self.dice.d4()):
                    items.append(self._generate_minor_magic())
            elif roll <= 99:
                items.append(self._generate_medium_magic())
            else:  # 100
                items.append(self._generate_major_magic())
        elif level == 11:
            if roll <= 31:
                return [Item(name="No Items", value=0, item_type="none")]
            elif roll <= 84:
                for _ in range(self.dice.d4()):
                    items.append(self._generate_minor_magic())
            elif roll <= 98:
                items.append(self._generate_medium_magic())
            else:  # 99-100
                items.append(self._generate_major_magic())
        elif level == 12:
            if roll <= 27:
                return [Item(name="No Items", value=0, item_type="none")]
            elif roll <= 82:
                for _ in range(self.dice.d6()):
                    items.append(self._generate_minor_magic())
            elif roll <= 97:
                items.append(self._generate_medium_magic())
            else:  # 98-100
                items.append(self._generate_major_magic())
        elif level >= 13 and level <= 20:
            # Simplified for levels 13-20
            if level <= 15:
                if roll <= 19:
                    return [Item(name="No Items", value=0, item_type="none")]
                elif roll <= 58:
                    for _ in range(self.dice.d6()):
                        items.append(self._generate_minor_magic())
                elif roll <= 92:
                    items.append(self._generate_medium_magic())
                else:  # 93-100
                    items.append(self._generate_major_magic())
            elif level <= 19:
                if roll <= 34:
                    return [Item(name="No Items", value=0, item_type="none")]
                elif roll <= 80:
                    for _ in range(self.dice.d4()):
                        items.append(self._generate_medium_magic())
                else:  # 81-100
                    items.append(self._generate_major_magic())
            else:  # level 20
                if roll <= 25:
                    return [Item(name="No Items", value=0, item_type="none")]
                elif roll <= 65:
                    for _ in range(self.dice.d4()):
                        items.append(self._generate_medium_magic())
                else:  # 66-100
                    for _ in range(self.dice.d3()):
                        items.append(self._generate_major_magic())
        else:
            return [Item(name="No Items", value=0, item_type="none")]

        return items if items else [Item(name="No Items", value=0, item_type="none")]

    def _generate_mundane(self) -> Item:
        """Generate a mundane (non-magical) item."""
        # For now, return a simple mundane item
        # TODO: Implement full mundane item table
        return Item(name="Masterwork item", value=300, item_type="mundane")

    def _generate_minor_magic(self) -> Item:
        """Generate a minor magic item."""
        roll = self.dice.d100()

        # DMG Table 7-1: Minor Magic Items
        if roll <= 4:
            return self._generate_magic_armor(ItemPower.MINOR)
        elif roll <= 9:
            return self._generate_magic_weapon(ItemPower.MINOR)
        elif roll <= 44:
            return self._generate_potion(ItemPower.MINOR)
        elif roll <= 46:
            return self._generate_ring(ItemPower.MINOR)
        elif roll <= 81:
            return self._generate_scroll(ItemPower.MINOR)
        elif roll <= 91:
            return self._generate_wand(ItemPower.MINOR)
        else:  # 92-100
            return self._generate_wonderous(ItemPower.MINOR)

    def _generate_medium_magic(self) -> Item:
        """Generate a medium magic item."""
        roll = self.dice.d100()

        # DMG Table 7-2: Medium Magic Items
        if roll <= 10:
            return self._generate_magic_armor(ItemPower.MEDIUM)
        elif roll <= 20:
            return self._generate_magic_weapon(ItemPower.MEDIUM)
        elif roll <= 30:
            return self._generate_potion(ItemPower.MEDIUM)
        elif roll <= 40:
            return self._generate_ring(ItemPower.MEDIUM)
        elif roll <= 50:
            return self._generate_rod(ItemPower.MEDIUM)
        elif roll <= 65:
            return self._generate_scroll(ItemPower.MEDIUM)
        elif roll <= 68:
            return self._generate_staff(ItemPower.MEDIUM)
        elif roll <= 83:
            return self._generate_wand(ItemPower.MEDIUM)
        else:  # 84-100
            return self._generate_wonderous(ItemPower.MEDIUM)

    def _generate_major_magic(self) -> Item:
        """Generate a major magic item."""
        roll = self.dice.d100()

        # DMG Table 7-3: Major Magic Items
        if roll <= 10:
            return self._generate_magic_armor(ItemPower.MAJOR)
        elif roll <= 20:
            return self._generate_magic_weapon(ItemPower.MAJOR)
        elif roll <= 25:
            return self._generate_potion(ItemPower.MAJOR)
        elif roll <= 35:
            return self._generate_ring(ItemPower.MAJOR)
        elif roll <= 45:
            return self._generate_rod(ItemPower.MAJOR)
        elif roll <= 55:
            return self._generate_scroll(ItemPower.MAJOR)
        elif roll <= 75:
            return self._generate_staff(ItemPower.MAJOR)
        elif roll <= 80:
            return self._generate_wand(ItemPower.MAJOR)
        else:  # 81-100
            return self._generate_wonderous(ItemPower.MAJOR)

    def _generate_potion(self, power: ItemPower) -> Item:
        """Generate a potion."""
        chart_name = {
            ItemPower.MINOR: "dmg/potions_minor",
            ItemPower.MEDIUM: "dmg/potions_medium",
            ItemPower.MAJOR: "dmg/potions_major"
        }[power]

        chart = self.chart_loader.load_chart_by_name(chart_name)
        roll = self.dice.d100()
        entry = chart.find_entry(roll)

        if entry:
            # Replace keywords if present
            name = self.keyword_replacer.replace(entry.name)
            return Item(name=name, value=entry.value, item_type="potion")

        return Item(name="Potion (unknown)", value=50, item_type="potion")

    def _generate_ring(self, power: ItemPower) -> Item:
        """Generate a ring."""
        chart_name = {
            ItemPower.MINOR: "dmg/rings_minor",
            ItemPower.MEDIUM: "dmg/rings_medium",
            ItemPower.MAJOR: "dmg/rings_major"
        }[power]

        chart = self.chart_loader.load_chart_by_name(chart_name)
        roll = self.dice.d100()
        entry = chart.find_entry(roll)

        if entry:
            name = self.keyword_replacer.replace(entry.name)
            return Item(name=name, value=entry.value, item_type="ring")

        return Item(name="Ring (unknown)", value=1000, item_type="ring")

    def _generate_wand(self, power: ItemPower) -> Item:
        """Generate a wand."""
        chart_name = {
            ItemPower.MINOR: "dmg/wands_minor",
            ItemPower.MEDIUM: "dmg/wands_medium",
            ItemPower.MAJOR: "dmg/wands_major"
        }[power]

        chart = self.chart_loader.load_chart_by_name(chart_name)
        roll = self.dice.d100()
        entry = chart.find_entry(roll)

        if entry:
            name = self.keyword_replacer.replace(entry.name)
            return Item(name=name, value=entry.value, item_type="wand")

        return Item(name="Wand (unknown)", value=750, item_type="wand")

    def _generate_wonderous(self, power: ItemPower) -> Item:
        """Generate a wonderous item."""
        chart_name = {
            ItemPower.MINOR: "dmg/wonderous_minor",
            ItemPower.MEDIUM: "dmg/wonderous_medium",
            ItemPower.MAJOR: "dmg/wonderous_major"
        }[power]

        chart = self.chart_loader.load_chart_by_name(chart_name)
        roll = self.dice.d100()
        entry = chart.find_entry(roll)

        if entry:
            name = self.keyword_replacer.replace(entry.name)
            return Item(name=name, value=entry.value, item_type="wonderous")

        return Item(name="Wonderous Item (unknown)", value=1000, item_type="wonderous")

    def _generate_scroll(self, power: ItemPower) -> Item:
        """Generate a scroll."""
        # Simplified - would need arcane/divine scroll tables
        return Item(name="Scroll (spell)", value=25, item_type="scroll")

    def _generate_rod(self, power: ItemPower) -> Item:
        """Generate a rod."""
        chart_name = {
            ItemPower.MEDIUM: "dmg/rods_medium",
            ItemPower.MAJOR: "dmg/rods_major"
        }[power]

        chart = self.chart_loader.load_chart_by_name(chart_name)
        roll = self.dice.d100()
        entry = chart.find_entry(roll)

        if entry:
            name = self.keyword_replacer.replace(entry.name)
            return Item(name=name, value=entry.value, item_type="rod")

        return Item(name="Rod (unknown)", value=5000, item_type="rod")

    def _generate_staff(self, power: ItemPower) -> Item:
        """Generate a staff."""
        chart_name = {
            ItemPower.MEDIUM: "dmg/staffs_medium",
            ItemPower.MAJOR: "dmg/staffs_major"
        }[power]

        chart = self.chart_loader.load_chart_by_name(chart_name)
        roll = self.dice.d100()
        entry = chart.find_entry(roll)

        if entry:
            name = self.keyword_replacer.replace(entry.name)
            return Item(name=name, value=entry.value, item_type="staff")

        return Item(name="Staff (unknown)", value=10000, item_type="staff")

    def _generate_magic_armor(self, power: ItemPower) -> Item:
        """Generate magic armor."""
        # Simplified - would need full armor generation with bonuses
        chart_name = {
            ItemPower.MINOR: "dmg/armor_minor",
            ItemPower.MEDIUM: "dmg/armor_medium",
            ItemPower.MAJOR: "dmg/armor_major"
        }[power]

        chart = self.chart_loader.load_chart_by_name(chart_name)
        roll = self.dice.d100()
        entry = chart.find_entry(roll)

        if entry:
            name = self.keyword_replacer.replace(entry.name)
            return Item(name=name, value=entry.value, item_type="armor")

        return Item(name="Magic Armor", value=1000, item_type="armor")

    def _generate_magic_weapon(self, power: ItemPower) -> Item:
        """Generate a magic weapon."""
        # Simplified - would need full weapon generation with bonuses
        chart_name = {
            ItemPower.MINOR: "dmg/melee_weapon_minor",
            ItemPower.MEDIUM: "dmg/melee_weapon_medium",
            ItemPower.MAJOR: "dmg/melee_weapon_major"
        }[power]

        chart = self.chart_loader.load_chart_by_name(chart_name)
        roll = self.dice.d100()
        entry = chart.find_entry(roll)

        if entry:
            name = self.keyword_replacer.replace(entry.name)
            return Item(name=name, value=entry.value, item_type="weapon")

        return Item(name="Magic Weapon", value=2000, item_type="weapon")
