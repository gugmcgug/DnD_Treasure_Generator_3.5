import pytest
from dnd_treasure.core.models import Item, Treasure, TreasureType


def test_item_creation():
    """Test creating an Item."""
    item = Item(name="Potion of Healing", value=50, item_type="potion")
    assert item.name == "Potion of Healing"
    assert item.value == 50
    assert item.item_type == "potion"


def test_item_display():
    """Test Item display method."""
    item = Item(name="Potion of Healing", value=50, item_type="potion")
    assert item.display() == "Potion of Healing (50 gp)"


def test_treasure_creation():
    """Test creating a Treasure."""
    treasure = Treasure(
        level=5,
        coins=["100 gp", "50 sp"],
        goods=["Gem worth 50 gp"],
        items=[Item(name="Potion of Healing", value=50, item_type="potion")]
    )
    assert treasure.level == 5
    assert len(treasure.coins) == 2
    assert len(treasure.goods) == 1
    assert len(treasure.items) == 1


def test_treasure_type_enum():
    """Test TreasureType enum."""
    assert TreasureType.NONE.value == 0
    assert TreasureType.STANDARD.value == 1
    assert TreasureType.DOUBLE.value == 2
    assert TreasureType.TRIPLE.value == 3
