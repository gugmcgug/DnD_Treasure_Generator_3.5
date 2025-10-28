import pytest
from dnd_treasure.data.models import ChartEntry, Chart


def test_chart_entry_creation():
    """Test creating a ChartEntry."""
    entry = ChartEntry(
        min_roll=1,
        max_roll=10,
        name="Potion of Healing",
        value=50
    )
    assert entry.min_roll == 1
    assert entry.max_roll == 10
    assert entry.name == "Potion of Healing"
    assert entry.value == 50


def test_chart_entry_with_variables():
    """Test ChartEntry with variable substitution."""
    entry = ChartEntry(
        min_roll=1,
        max_roll=5,
        name="Potion of Protection from {alignment}",
        value=50,
        variables={"alignment": "dmg_alignments"}
    )
    assert "{alignment}" in entry.name
    assert entry.variables["alignment"] == "dmg_alignments"


def test_chart_creation():
    """Test creating a Chart."""
    chart = Chart(
        name="DMG Minor Potions",
        source="DMG",
        page=230,
        table="7-17",
        roll_die="d100",
        entries=[
            ChartEntry(min_roll=1, max_roll=10, name="Potion A", value=50),
            ChartEntry(min_roll=11, max_roll=20, name="Potion B", value=75),
        ]
    )
    assert chart.name == "DMG Minor Potions"
    assert len(chart.entries) == 2


def test_chart_find_entry():
    """Test finding an entry by roll."""
    chart = Chart(
        name="Test Chart",
        source="DMG",
        entries=[
            ChartEntry(min_roll=1, max_roll=50, name="Item A", value=10),
            ChartEntry(min_roll=51, max_roll=100, name="Item B", value=20),
        ]
    )
    entry = chart.find_entry(25)
    assert entry.name == "Item A"

    entry = chart.find_entry(75)
    assert entry.name == "Item B"
