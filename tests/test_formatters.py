import pytest
from dnd_treasure.core.models import Treasure, Item
from dnd_treasure.formatters.text import TextFormatter


def test_format_empty_treasure():
    """Test formatting empty treasure."""
    treasure = Treasure(
        level=5,
        coins=["No Coins"],
        goods=["No Goods"],
        items=[Item(name="No Items", value=0, item_type="none")]
    )

    formatter = TextFormatter()
    output = formatter.format(treasure)

    assert "Level 5" in output
    assert "No Coins" in output
    assert "No Goods" in output
    assert "No Items" in output


def test_format_treasure_with_coins():
    """Test formatting treasure with coins."""
    treasure = Treasure(
        level=10,
        coins=["100 gp", "50 sp"],
        goods=["No Goods"],
        items=[Item(name="No Items", value=0, item_type="none")]
    )

    formatter = TextFormatter()
    output = formatter.format(treasure)

    assert "100 gp" in output
    assert "50 sp" in output


def test_format_treasure_with_items():
    """Test formatting treasure with magic items."""
    treasure = Treasure(
        level=15,
        coins=["1000 gp"],
        goods=["Gem worth 100 gp"],
        items=[
            Item(name="Potion of Healing", value=50, item_type="potion"),
            Item(name="+1 Longsword", value=2315, item_type="weapon")
        ]
    )

    formatter = TextFormatter()
    output = formatter.format(treasure)

    assert "Potion of Healing" in output
    assert "+1 Longsword" in output
    assert "Gem worth 100 gp" in output
