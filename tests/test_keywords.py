import pytest
from dnd_treasure.core.keywords import KeywordReplacer
from dnd_treasure.core.dice import Dice
from dnd_treasure.data.loader import ChartLoader


def test_replace_alignment_keyword(tmp_path):
    """Test replacing {alignment} keyword."""
    # Create test alignment chart
    import yaml
    charts_dir = tmp_path / "charts" / "dmg"
    charts_dir.mkdir(parents=True)

    chart_data = {
        "name": "Alignments",
        "source": "DMG",
        "roll_die": "d3",
        "entries": [
            {"min_roll": 1, "max_roll": 1, "name": "Lawful Good", "value": 0},
            {"min_roll": 2, "max_roll": 2, "name": "Chaotic Evil", "value": 0},
            {"min_roll": 3, "max_roll": 3, "name": "Neutral", "value": 0},
        ]
    }
    with open(charts_dir / "alignments.yaml", 'w') as f:
        yaml.dump(chart_data, f)

    loader = ChartLoader(tmp_path / "charts")
    dice = Dice(seed=42)  # Fixed seed for reproducible test
    replacer = KeywordReplacer(loader, dice)

    result = replacer.replace("Potion of Protection from {alignment}")
    assert "Potion of Protection from" in result
    assert "{alignment}" not in result


def test_no_keywords():
    """Test that strings without keywords pass through unchanged."""
    loader = ChartLoader()
    dice = Dice()
    replacer = KeywordReplacer(loader, dice)

    result = replacer.replace("Potion of Healing")
    assert result == "Potion of Healing"


def test_multiple_keywords(tmp_path):
    """Test replacing multiple keywords in one string."""
    # Create test charts
    import yaml
    charts_dir = tmp_path / "charts" / "dmg"
    charts_dir.mkdir(parents=True)

    alignment_data = {
        "name": "Alignments",
        "source": "DMG",
        "roll_die": "d2",
        "entries": [
            {"min_roll": 1, "max_roll": 1, "name": "Good", "value": 0},
            {"min_roll": 2, "max_roll": 2, "name": "Evil", "value": 0},
        ]
    }
    energy_data = {
        "name": "Energy Types",
        "source": "DMG",
        "roll_die": "d2",
        "entries": [
            {"min_roll": 1, "max_roll": 1, "name": "Fire", "value": 0},
            {"min_roll": 2, "max_roll": 2, "name": "Cold", "value": 0},
        ]
    }

    with open(charts_dir / "alignments.yaml", 'w') as f:
        yaml.dump(alignment_data, f)
    with open(charts_dir / "energy.yaml", 'w') as f:
        yaml.dump(energy_data, f)

    loader = ChartLoader(tmp_path / "charts")
    dice = Dice(seed=42)
    replacer = KeywordReplacer(loader, dice)

    result = replacer.replace("Ring of {alignment} {energy}")
    assert "{alignment}" not in result
    assert "{energy}" not in result
