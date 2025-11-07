"""Main treasure generation orchestrator."""

from pathlib import Path
from typing import List, Optional

from dnd_treasure.core.dice import Dice
from dnd_treasure.core.coins import CoinGenerator
from dnd_treasure.core.goods import GoodsGenerator
from dnd_treasure.core.items import ItemGenerator
from dnd_treasure.core.keywords import KeywordReplacer
from dnd_treasure.core.models import Treasure, TreasureType, Item
from dnd_treasure.data.loader import ChartLoader


class TreasureGenerator:
    """Main class for generating D&D treasure hoards."""

    def __init__(
        self,
        seed: Optional[int] = None,
        charts_path: Optional[Path] = None
    ):
        """
        Initialize treasure generator.

        Args:
            seed: Optional random seed for reproducible results.
            charts_path: Optional path to charts directory.
        """
        self.dice = Dice(seed)
        self.chart_loader = ChartLoader(charts_path)
        self.keyword_replacer = KeywordReplacer(self.chart_loader, self.dice)
        self.coin_generator = CoinGenerator(self.dice)
        self.goods_generator = GoodsGenerator(self.dice, self.chart_loader)
        self.item_generator = ItemGenerator(self.dice, self.chart_loader, self.keyword_replacer)

    def generate(
        self,
        level: int,
        coins: TreasureType = TreasureType.STANDARD,
        goods: TreasureType = TreasureType.STANDARD,
        items: TreasureType = TreasureType.STANDARD,
    ) -> Treasure:
        """
        Generate a complete treasure hoard.

        Args:
            level: Encounter level (1-20).
            coins: Coin generation type.
            goods: Goods generation type.
            items: Items generation type.

        Returns:
            Generated Treasure object.
        """
        return Treasure(
            level=level,
            coins=self._generate_coins(level, coins),
            goods=self._generate_goods(level, goods),
            items=self._generate_items(level, items),
        )

    def _generate_coins(self, level: int, treasure_type: TreasureType) -> List[str]:
        """Generate coins for the treasure."""
        return self.coin_generator.generate(level, treasure_type)

    def _generate_goods(self, level: int, treasure_type: TreasureType) -> List[str]:
        """Generate goods (gems and art objects) for the treasure."""
        return self.goods_generator.generate(level, treasure_type)

    def _generate_items(self, level: int, treasure_type: TreasureType) -> List[Item]:
        """Generate magic items for the treasure."""
        return self.item_generator.generate(level, treasure_type)
