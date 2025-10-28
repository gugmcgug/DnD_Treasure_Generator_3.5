import pytest
from dnd_treasure.core.generator import TreasureGenerator
from dnd_treasure.core.models import Treasure, TreasureType


def test_generate_empty_treasure():
    """Test generating completely empty treasure."""
    generator = TreasureGenerator(seed=42)

    treasure = generator.generate(
        level=5,
        coins=TreasureType.NONE,
        goods=TreasureType.NONE,
        items=TreasureType.NONE
    )

    assert isinstance(treasure, Treasure)
    assert treasure.level == 5
    assert treasure.coins == ["No Coins"]
    assert treasure.goods == ["No Goods"]
    assert treasure.items[0].name == "No Items"


def test_generate_with_coins_only():
    """Test generating treasure with only coins."""
    generator = TreasureGenerator(seed=42)

    treasure = generator.generate(
        level=5,
        coins=TreasureType.STANDARD,
        goods=TreasureType.NONE,
        items=TreasureType.NONE
    )

    assert len(treasure.coins) >= 1
    assert treasure.goods == ["No Goods"]


def test_generate_full_treasure():
    """Test generating treasure with all components."""
    generator = TreasureGenerator(seed=42)

    treasure = generator.generate(
        level=10,
        coins=TreasureType.STANDARD,
        goods=TreasureType.STANDARD,
        items=TreasureType.STANDARD
    )

    assert isinstance(treasure, Treasure)
    assert treasure.level == 10
    # Should have some treasure (may be "No X" but lists should exist)
    assert treasure.coins is not None
    assert treasure.goods is not None
    assert treasure.items is not None
