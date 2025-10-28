import pytest
import yaml
from pathlib import Path
from dnd_treasure.data.loader import ChartLoader
from dnd_treasure.data.models import Chart


@pytest.fixture
def test_chart_file(tmp_path):
    """Create a temporary test chart file."""
    chart_data = {
        "name": "Test Potions",
        "source": "DMG",
        "page": 230,
        "table": "7-17",
        "roll_die": "d100",
        "entries": [
            {"min_roll": 1, "max_roll": 50, "name": "Potion A", "value": 50},
            {"min_roll": 51, "max_roll": 100, "name": "Potion B", "value": 100},
        ]
    }
    chart_file = tmp_path / "test_potions.yaml"
    with open(chart_file, 'w') as f:
        yaml.dump(chart_data, f)
    return chart_file


def test_load_chart_from_file(test_chart_file):
    """Test loading a chart from a YAML file."""
    loader = ChartLoader()
    chart = loader.load_chart(test_chart_file)

    assert isinstance(chart, Chart)
    assert chart.name == "Test Potions"
    assert chart.source == "DMG"
    assert len(chart.entries) == 2


def test_chart_caching(test_chart_file):
    """Test that charts are cached after first load."""
    loader = ChartLoader()
    chart1 = loader.load_chart(test_chart_file)
    chart2 = loader.load_chart(test_chart_file)

    # Should be the same object (cached)
    assert chart1 is chart2


def test_load_chart_by_name(tmp_path):
    """Test loading a chart by name from charts directory."""
    charts_dir = tmp_path / "charts" / "dmg"
    charts_dir.mkdir(parents=True)

    chart_data = {
        "name": "DMG Armor",
        "source": "DMG",
        "entries": [
            {"min_roll": 1, "max_roll": 100, "name": "Leather Armor", "value": 160},
        ]
    }
    chart_file = charts_dir / "armor.yaml"
    with open(chart_file, 'w') as f:
        yaml.dump(chart_data, f)

    loader = ChartLoader(charts_dir.parent)
    chart = loader.load_chart_by_name("dmg/armor")

    assert chart.name == "DMG Armor"
