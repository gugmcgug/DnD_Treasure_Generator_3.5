import pytest
from dnd_treasure.core.coins import CoinGenerator
from dnd_treasure.core.dice import Dice
from dnd_treasure.core.models import TreasureType


def test_no_coins():
    """Test generating no coins."""
    dice = Dice(seed=42)
    generator = CoinGenerator(dice)

    result = generator.generate(level=5, treasure_type=TreasureType.NONE)
    assert result == ["No Coins"]


def test_standard_coins_level_1():
    """Test generating standard coins for level 1."""
    dice = Dice(seed=42)
    generator = CoinGenerator(dice)

    result = generator.generate(level=1, treasure_type=TreasureType.STANDARD)
    assert len(result) == 1
    assert any(coin_type in result[0] for coin_type in ["cp", "sp", "gp", "pp", "No Coins"])


def test_double_coins():
    """Test generating double coins."""
    dice = Dice(seed=42)
    generator = CoinGenerator(dice)

    result = generator.generate(level=5, treasure_type=TreasureType.DOUBLE)
    # Should generate 2 sets of coins (may include "No Coins")
    assert len(result) >= 1 and len(result) <= 2


def test_triple_coins():
    """Test generating triple coins."""
    dice = Dice(seed=42)
    generator = CoinGenerator(dice)

    result = generator.generate(level=5, treasure_type=TreasureType.TRIPLE)
    # Should generate 3 sets of coins (may include "No Coins")
    assert len(result) >= 1 and len(result) <= 3


def test_coin_format():
    """Test coin output format."""
    dice = Dice(seed=10)
    generator = CoinGenerator(dice)

    result = generator.generate(level=10, treasure_type=TreasureType.STANDARD)
    # Should be in format "123 gp" or "No Coins"
    if result[0] != "No Coins":
        assert any(coin_type in result[0] for coin_type in ["cp", "sp", "gp", "pp"])
        # Check format: number + space + coin type
        parts = result[0].split()
        assert len(parts) == 2
        assert parts[0].isdigit()
