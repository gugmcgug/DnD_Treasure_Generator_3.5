import pytest
from dnd_treasure.core.dice import Dice


def test_dice_roll_returns_integer():
    """Test that roll() returns an integer."""
    dice = Dice()
    result = dice.roll(6)
    assert isinstance(result, int)


def test_dice_roll_within_range():
    """Test that roll() returns value between 1 and max."""
    dice = Dice()
    for _ in range(100):
        result = dice.roll(6)
        assert 1 <= result <= 6


def test_dice_roll_multiple_dice():
    """Test rolling multiple dice (e.g., 3d6)."""
    dice = Dice()
    result = dice.roll(num_dice=3, num_sides=6)
    assert isinstance(result, int)
    assert 3 <= result <= 18


def test_d100():
    """Test d100() helper method."""
    dice = Dice()
    for _ in range(100):
        result = dice.d100()
        assert 1 <= result <= 100


def test_d20():
    """Test d20() helper method."""
    dice = Dice()
    for _ in range(100):
        result = dice.d20()
        assert 1 <= result <= 20
