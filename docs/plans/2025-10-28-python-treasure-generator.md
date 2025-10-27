# D&D 3.5 Treasure Generator - Python Implementation Plan

> **For Claude:** Use `${SUPERPOWERS_SKILLS_ROOT}/skills/collaboration/executing-plans/SKILL.md` to implement this plan task-by-task.

**Goal:** Convert the VB.NET D&D 3.5 Treasure Generator to a Python CLI tool with extensible architecture for adding new sources.

**Architecture:** Table-driven random generation using YAML data files, dataclasses for type safety, modular design separating dice rolling, data loading, generation logic, and output formatting.

**Tech Stack:** Python 3.10+, PyYAML for data files, click for CLI, pytest for testing, pydantic for validation

---

## Task 1: Project Structure & Dependencies

**Files:**
- Create: `dnd_treasure/__init__.py`
- Create: `dnd_treasure/core/__init__.py`
- Create: `dnd_treasure/data/__init__.py`
- Create: `dnd_treasure/formatters/__init__.py`
- Create: `pyproject.toml`
- Create: `requirements.txt`
- Create: `tests/__init__.py`
- Create: `.gitignore`

**Step 1: Create project structure**

```bash
mkdir -p dnd_treasure/core dnd_treasure/data/charts/dmg dnd_treasure/formatters tests
touch dnd_treasure/__init__.py dnd_treasure/core/__init__.py dnd_treasure/data/__init__.py dnd_treasure/formatters/__init__.py tests/__init__.py
```

**Step 2: Write pyproject.toml**

Create `pyproject.toml`:

```toml
[project]
name = "dnd-treasure"
version = "0.1.0"
description = "D&D 3.5 Treasure Generator"
requires-python = ">=3.10"
dependencies = [
    "pyyaml>=6.0",
    "click>=8.1.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]

[project.scripts]
dnd-treasure = "dnd_treasure.cli:main"

[build-system]
requires = ["setuptools>=65.0"]
build-backend = "setuptools.build_meta"
```

**Step 3: Write requirements.txt**

Create `requirements.txt`:

```
pyyaml>=6.0
click>=8.1.0
pydantic>=2.0.0
pytest>=7.0.0
pytest-cov>=4.0.0
```

**Step 4: Write .gitignore**

Create `.gitignore`:

```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.pytest_cache/
.coverage
htmlcov/
.venv/
venv/
ENV/
.idea/
.vscode/
*.swp
*.swo
*~
```

**Step 5: Commit**

```bash
git init
git add .
git commit -m "feat: initialize Python project structure"
```

---

## Task 2: Dice Rolling Module

**Files:**
- Create: `dnd_treasure/core/dice.py`
- Create: `tests/test_dice.py`

**Step 1: Write the failing test**

Create `tests/test_dice.py`:

```python
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
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_dice.py -v`

Expected: FAIL with "ModuleNotFoundError: No module named 'dnd_treasure.core.dice'"

**Step 3: Write minimal implementation**

Create `dnd_treasure/core/dice.py`:

```python
"""Dice rolling utilities for D&D treasure generation."""

import random
from typing import Optional


class Dice:
    """Handles all dice rolling operations."""

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize dice roller.

        Args:
            seed: Optional random seed for reproducible results in tests.
        """
        self._random = random.Random(seed)

    def roll(self, num_sides: int, num_dice: int = 1) -> int:
        """
        Roll dice and return the sum.

        Args:
            num_sides: Number of sides on each die.
            num_dice: Number of dice to roll (default 1).

        Returns:
            Sum of all dice rolled.
        """
        return sum(self._random.randint(1, num_sides) for _ in range(num_dice))

    def d100(self, num_dice: int = 1) -> int:
        """Roll d100 (1-100)."""
        return self.roll(100, num_dice)

    def d20(self, num_dice: int = 1) -> int:
        """Roll d20 (1-20)."""
        return self.roll(20, num_dice)

    def d12(self, num_dice: int = 1) -> int:
        """Roll d12 (1-12)."""
        return self.roll(12, num_dice)

    def d10(self, num_dice: int = 1) -> int:
        """Roll d10 (1-10)."""
        return self.roll(10, num_dice)

    def d8(self, num_dice: int = 1) -> int:
        """Roll d8 (1-8)."""
        return self.roll(8, num_dice)

    def d6(self, num_dice: int = 1) -> int:
        """Roll d6 (1-6)."""
        return self.roll(6, num_dice)

    def d4(self, num_dice: int = 1) -> int:
        """Roll d4 (1-4)."""
        return self.roll(4, num_dice)

    def d3(self, num_dice: int = 1) -> int:
        """Roll d3 (1-3)."""
        return self.roll(3, num_dice)

    def d2(self, num_dice: int = 1) -> int:
        """Roll d2 (1-2)."""
        return self.roll(2, num_dice)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_dice.py -v`

Expected: PASS (all tests green)

**Step 5: Commit**

```bash
git add dnd_treasure/core/dice.py tests/test_dice.py
git commit -m "feat: add dice rolling module with d4-d100 support"
```

---

## Task 3: Data Models

**Files:**
- Create: `dnd_treasure/core/models.py`
- Create: `tests/test_models.py`

**Step 1: Write the failing test**

Create `tests/test_models.py`:

```python
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
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_models.py -v`

Expected: FAIL with "ModuleNotFoundError: No module named 'dnd_treasure.core.models'"

**Step 3: Write minimal implementation**

Create `dnd_treasure/core/models.py`:

```python
"""Data models for D&D treasure generation."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class TreasureType(Enum):
    """Treasure generation multiplier types."""
    NONE = 0
    STANDARD = 1
    DOUBLE = 2
    TRIPLE = 3
    HALF = 0.5
    TEN_PERCENT = 0.1


class CoinType(Enum):
    """Coin denominations."""
    CP = 1      # Copper pieces
    SP = 10     # Silver pieces
    GP = 100    # Gold pieces
    PP = 1000   # Platinum pieces


class ItemPower(Enum):
    """Magic item power levels."""
    MINOR = 1
    MEDIUM = 2
    MAJOR = 3


class Source(Enum):
    """Source books for treasure generation."""
    DMG = 1  # Dungeon Master's Guide
    EPH = 2  # Expanded Psionics Handbook
    MIC = 3  # Magic Item Compendium


@dataclass
class Item:
    """Represents a treasure item."""
    name: str
    value: int
    item_type: str
    flag: int = 0

    def display(self) -> str:
        """Format item for display."""
        return f"{self.name} ({self.value} gp)"


@dataclass
class Treasure:
    """Represents a complete treasure hoard."""
    level: int
    coins: List[str] = field(default_factory=list)
    goods: List[str] = field(default_factory=list)
    items: List[Item] = field(default_factory=list)

    def is_empty(self) -> bool:
        """Check if treasure is empty."""
        return (
            len(self.coins) == 0 and
            len(self.goods) == 0 and
            len(self.items) == 0
        )
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_models.py -v`

Expected: PASS (all tests green)

**Step 5: Commit**

```bash
git add dnd_treasure/core/models.py tests/test_models.py
git commit -m "feat: add data models for items and treasure"
```

---

## Task 4: Chart Data Structures

**Files:**
- Create: `dnd_treasure/data/models.py`
- Create: `tests/test_data_models.py`

**Step 1: Write the failing test**

Create `tests/test_data_models.py`:

```python
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
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_data_models.py -v`

Expected: FAIL with "ModuleNotFoundError: No module named 'dnd_treasure.data.models'"

**Step 3: Write minimal implementation**

Create `dnd_treasure/data/models.py`:

```python
"""Data models for chart structures."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ChartEntry:
    """Represents a single entry in a treasure chart."""
    min_roll: int
    max_roll: int
    name: str
    value: int
    flag: int = 0
    variables: Optional[Dict[str, str]] = None

    def matches_roll(self, roll: int) -> bool:
        """Check if a roll falls within this entry's range."""
        return self.min_roll <= roll <= self.max_roll


@dataclass
class Chart:
    """Represents a complete treasure generation chart."""
    name: str
    source: str
    entries: List[ChartEntry]
    page: Optional[int] = None
    table: Optional[str] = None
    roll_die: str = "d100"

    def find_entry(self, roll: int) -> Optional[ChartEntry]:
        """
        Find the chart entry matching a given roll.

        Args:
            roll: The dice roll value.

        Returns:
            The matching ChartEntry, or None if not found.
        """
        for entry in self.entries:
            if entry.matches_roll(roll):
                return entry
        return None
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_data_models.py -v`

Expected: PASS (all tests green)

**Step 5: Commit**

```bash
git add dnd_treasure/data/models.py tests/test_data_models.py
git commit -m "feat: add chart data models with roll matching"
```

---

## Task 5: YAML Chart Loader

**Files:**
- Create: `dnd_treasure/data/loader.py`
- Create: `tests/test_loader.py`
- Create: `dnd_treasure/data/charts/dmg/test_chart.yaml` (test fixture)

**Step 1: Write the failing test**

Create `tests/test_loader.py`:

```python
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
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_loader.py -v`

Expected: FAIL with "ModuleNotFoundError: No module named 'dnd_treasure.data.loader'"

**Step 3: Write minimal implementation**

Create `dnd_treasure/data/loader.py`:

```python
"""Chart loading and caching utilities."""

import yaml
from pathlib import Path
from typing import Dict, Union

from dnd_treasure.data.models import Chart, ChartEntry


class ChartLoader:
    """Loads and caches treasure generation charts."""

    def __init__(self, charts_base_path: Union[str, Path, None] = None):
        """
        Initialize the chart loader.

        Args:
            charts_base_path: Base path for chart files. Defaults to package data/charts.
        """
        if charts_base_path is None:
            charts_base_path = Path(__file__).parent / "charts"
        self.charts_base_path = Path(charts_base_path)
        self._cache: Dict[str, Chart] = {}

    def load_chart(self, file_path: Union[str, Path]) -> Chart:
        """
        Load a chart from a YAML file.

        Args:
            file_path: Path to the chart YAML file.

        Returns:
            Loaded Chart object.
        """
        file_path = Path(file_path)
        cache_key = str(file_path)

        # Return cached chart if available
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Load from file
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

        # Convert entries to ChartEntry objects
        entries = [
            ChartEntry(
                min_roll=entry["min_roll"],
                max_roll=entry["max_roll"],
                name=entry["name"],
                value=entry["value"],
                flag=entry.get("flag", 0),
                variables=entry.get("variables")
            )
            for entry in data["entries"]
        ]

        # Create Chart object
        chart = Chart(
            name=data["name"],
            source=data["source"],
            entries=entries,
            page=data.get("page"),
            table=data.get("table"),
            roll_die=data.get("roll_die", "d100")
        )

        # Cache and return
        self._cache[cache_key] = chart
        return chart

    def load_chart_by_name(self, chart_name: str) -> Chart:
        """
        Load a chart by its relative name (e.g., 'dmg/armor').

        Args:
            chart_name: Relative path without .yaml extension.

        Returns:
            Loaded Chart object.
        """
        file_path = self.charts_base_path / f"{chart_name}.yaml"
        return self.load_chart(file_path)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_loader.py -v`

Expected: PASS (all tests green)

**Step 5: Commit**

```bash
git add dnd_treasure/data/loader.py tests/test_loader.py
git commit -m "feat: add YAML chart loader with caching"
```

---

## Task 6: Convert Sample Charts to YAML

**Files:**
- Create: `dnd_treasure/data/charts/dmg/armor.yaml`
- Create: `dnd_treasure/data/charts/dmg/potions_minor.yaml`
- Create: `dnd_treasure/data/charts/dmg/alignments.yaml`
- Create: `scripts/convert_charts.py` (conversion utility)

**Step 1: Write chart conversion script**

Create `scripts/convert_charts.py`:

```python
"""Convert VB chart files to YAML format."""

import yaml
from pathlib import Path


def parse_chart_file(file_path: Path) -> dict:
    """Parse a VB chart .txt file into a dictionary."""
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('//')]

    num_entries = int(lines[0])
    entries = []

    for i in range(1, num_entries + 1):
        parts = lines[i].split('|')
        entry = {
            "min_roll": int(parts[0]),
            "max_roll": int(parts[1]),
            "name": parts[2],
            "value": int(parts[3])
        }
        if len(parts) > 4:
            entry["flag"] = int(parts[4])

        entries.append(entry)

    # Extract metadata from comments
    metadata_lines = [line for line in lines[num_entries + 1:] if line.startswith('//')]
    source = "DMG"
    page = None
    table = None

    for line in metadata_lines:
        if "Page" in line:
            page = int(''.join(filter(str.isdigit, line)))
        if "Table" in line:
            table = line.split("Table")[-1].strip().strip(':')

    return {
        "entries": entries,
        "source": source,
        "page": page,
        "table": table
    }


def convert_chart(input_path: Path, output_path: Path, chart_name: str):
    """Convert a single chart file to YAML."""
    data = parse_chart_file(input_path)
    data["name"] = chart_name
    data["roll_die"] = "d100"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    print(f"Converted {input_path.name} -> {output_path}")


if __name__ == "__main__":
    # Convert sample charts
    charts_base = Path("Treasure_Generator/bin/Debug/Charts")
    output_base = Path("dnd_treasure/data/charts/dmg")

    conversions = [
        ("DMGArmor.txt", "armor.yaml", "DMG Armor Types"),
        ("DMGPotionsMin.txt", "potions_minor.yaml", "DMG Minor Potions"),
        ("DMGAlignments.txt", "alignments.yaml", "DMG Alignments"),
    ]

    for input_file, output_file, name in conversions:
        convert_chart(
            charts_base / input_file,
            output_base / output_file,
            name
        )
```

**Step 2: Run conversion script**

Run: `python scripts/convert_charts.py`

Expected: Creates 3 YAML files in `dnd_treasure/data/charts/dmg/`

**Step 3: Manually create alignments.yaml (simple list)**

Create `dnd_treasure/data/charts/dmg/alignments.yaml`:

```yaml
name: DMG Alignments
source: DMG
page: 216
roll_die: d9
entries:
  - min_roll: 1
    max_roll: 1
    name: Lawful Good
    value: 0
  - min_roll: 2
    max_roll: 2
    name: Neutral Good
    value: 0
  - min_roll: 3
    max_roll: 3
    name: Chaotic Good
    value: 0
  - min_roll: 4
    max_roll: 4
    name: Lawful Neutral
    value: 0
  - min_roll: 5
    max_roll: 5
    name: Neutral
    value: 0
  - min_roll: 6
    max_roll: 6
    name: Chaotic Neutral
    value: 0
  - min_roll: 7
    max_roll: 7
    name: Lawful Evil
    value: 0
  - min_roll: 8
    max_roll: 8
    name: Neutral Evil
    value: 0
  - min_roll: 9
    max_roll: 9
    name: Chaotic Evil
    value: 0
```

**Step 4: Verify YAML files load correctly**

Run: `pytest tests/test_loader.py -v`

Expected: PASS

**Step 5: Commit**

```bash
git add scripts/convert_charts.py dnd_treasure/data/charts/dmg/*.yaml
git commit -m "feat: add chart conversion script and sample YAML charts"
```

---

## Task 7: Keyword Substitution System

**Files:**
- Create: `dnd_treasure/core/keywords.py`
- Create: `tests/test_keywords.py`

**Step 1: Write the failing test**

Create `tests/test_keywords.py`:

```python
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
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_keywords.py -v`

Expected: FAIL with "ModuleNotFoundError: No module named 'dnd_treasure.core.keywords'"

**Step 3: Write minimal implementation**

Create `dnd_treasure/core/keywords.py`:

```python
"""Keyword substitution for dynamic item names."""

import re
from typing import Dict

from dnd_treasure.core.dice import Dice
from dnd_treasure.data.loader import ChartLoader


class KeywordReplacer:
    """Handles replacement of keywords in item names with random values."""

    # Map keywords to chart file names
    KEYWORD_CHARTS: Dict[str, str] = {
        "alignment": "dmg/alignments",
        "energy": "dmg/energy",
        "creature": "dmg/bane_creature_type",
    }

    def __init__(self, chart_loader: ChartLoader, dice: Dice):
        """
        Initialize keyword replacer.

        Args:
            chart_loader: Chart loader for accessing reference charts.
            dice: Dice roller for random selection.
        """
        self.loader = chart_loader
        self.dice = dice

    def replace(self, text: str) -> str:
        """
        Replace all keywords in text with random values.

        Args:
            text: Text containing keywords in {keyword} format.

        Returns:
            Text with keywords replaced.
        """
        # Find all keywords in the text
        keywords = re.findall(r'\{(\w+)\}', text)

        # Replace each keyword
        result = text
        for keyword in keywords:
            if keyword in self.KEYWORD_CHARTS:
                replacement = self._get_keyword_value(keyword)
                result = result.replace(f"{{{keyword}}}", replacement)

        return result

    def _get_keyword_value(self, keyword: str) -> str:
        """
        Get a random value for a keyword by rolling on its chart.

        Args:
            keyword: The keyword to replace.

        Returns:
            Random value from the keyword's chart.
        """
        chart_name = self.KEYWORD_CHARTS[keyword]
        chart = self.loader.load_chart_by_name(chart_name)

        # Determine roll based on chart's roll_die
        if chart.roll_die.startswith('d'):
            die_size = int(chart.roll_die[1:])
            roll = self.dice.roll(die_size)
        else:
            roll = self.dice.d100()

        entry = chart.find_entry(roll)
        return entry.name if entry else f"<{keyword}>"
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_keywords.py -v`

Expected: PASS (all tests green)

**Step 5: Commit**

```bash
git add dnd_treasure/core/keywords.py tests/test_keywords.py
git commit -m "feat: add keyword substitution system for dynamic item names"
```

---

## Task 8: Coin Generation Logic

**Files:**
- Create: `dnd_treasure/core/coins.py`
- Create: `tests/test_coins.py`

**Step 1: Write the failing test**

Create `tests/test_coins.py`:

```python
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
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_coins.py -v`

Expected: FAIL with "ModuleNotFoundError: No module named 'dnd_treasure.core.coins'"

**Step 3: Write minimal implementation**

Create `dnd_treasure/core/coins.py`:

```python
"""Coin generation logic for treasure hoards."""

from typing import List

from dnd_treasure.core.dice import Dice
from dnd_treasure.core.models import TreasureType, CoinType


class CoinGenerator:
    """Generates coins based on treasure level and type."""

    def __init__(self, dice: Dice):
        """
        Initialize coin generator.

        Args:
            dice: Dice roller for random generation.
        """
        self.dice = dice

    def generate(
        self,
        level: int,
        treasure_type: TreasureType,
        percentage: float = 1.0
    ) -> List[str]:
        """
        Generate coins for a treasure hoard.

        Args:
            level: Encounter level (1-20).
            treasure_type: Type of treasure (NONE, STANDARD, DOUBLE, TRIPLE).
            percentage: Multiplier for coin amounts (default 1.0).

        Returns:
            List of coin strings (e.g., ["100 gp", "50 sp"]).
        """
        if treasure_type == TreasureType.NONE:
            return ["No Coins"]

        coins = []

        # Generate first set
        coin_str = self._generate_single(level, percentage)
        if coin_str != "No Coins":
            coins.append(coin_str)

        # Generate additional sets for double/triple
        if treasure_type == TreasureType.DOUBLE:
            coin_str = self._generate_single(level, percentage)
            if coin_str != "No Coins":
                coins.append(coin_str)
        elif treasure_type == TreasureType.TRIPLE:
            for _ in range(2):
                coin_str = self._generate_single(level, percentage)
                if coin_str != "No Coins":
                    coins.append(coin_str)

        return coins if coins else ["No Coins"]

    def _generate_single(self, level: int, percentage: float = 1.0) -> str:
        """
        Generate a single set of coins based on level.

        This implements the DMG treasure tables for coin generation.

        Args:
            level: Encounter level (1-20).
            percentage: Multiplier for coin amounts.

        Returns:
            Coin string (e.g., "100 gp") or "No Coins".
        """
        roll = self.dice.d100()
        value = 0
        coin_type = None

        # Implement DMG coin tables by level
        # This is a simplified version - full implementation would have all 20 levels
        if level == 1:
            if 1 <= roll <= 14:
                return "No Coins"
            elif 15 <= roll <= 29:
                value = self._roll_coins(1, 6, 1000)
                coin_type = "cp"
            elif 30 <= roll <= 52:
                value = self._roll_coins(1, 8, 100)
                coin_type = "sp"
            elif 53 <= roll <= 95:
                value = self._roll_coins(2, 8, 10)
                coin_type = "gp"
            else:  # 96-100
                value = self._roll_coins(1, 4, 10)
                coin_type = "pp"
        elif level <= 4:
            # Simplified - higher levels would have similar tables
            if 1 <= roll <= 10:
                return "No Coins"
            elif 11 <= roll <= 30:
                value = self._roll_coins(2, 10, 1000)
                coin_type = "cp"
            elif 31 <= roll <= 60:
                value = self._roll_coins(4, 8, 100)
                coin_type = "sp"
            elif 61 <= roll <= 95:
                value = self._roll_coins(4, 10, 10)
                coin_type = "gp"
            else:
                value = self._roll_coins(2, 8, 10)
                coin_type = "pp"
        else:
            # Higher levels (simplified)
            if 1 <= roll <= 10:
                return "No Coins"
            elif 11 <= roll <= 25:
                value = self._roll_coins(2, 10, 1000)
                coin_type = "sp"
            elif 26 <= roll <= 75:
                value = self._roll_coins(6, 4, 100)
                coin_type = "gp"
            else:
                value = self._roll_coins(5, 6, 10)
                coin_type = "pp"

        if value > 0 and coin_type:
            value = int(value * percentage)
            return f"{value} {coin_type}"

        return "No Coins"

    def _roll_coins(self, num_dice: int, die_size: int, multiplier: int) -> int:
        """
        Roll dice for coin generation.

        Args:
            num_dice: Number of dice to roll.
            die_size: Size of each die.
            multiplier: Multiply result by this value.

        Returns:
            Total coins rolled.
        """
        return self.dice.roll(die_size, num_dice) * multiplier
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_coins.py -v`

Expected: PASS (all tests green)

**Step 5: Commit**

```bash
git add dnd_treasure/core/coins.py tests/test_coins.py
git commit -m "feat: add coin generation with DMG tables"
```

---

## Task 9: Main Treasure Generator

**Files:**
- Create: `dnd_treasure/core/generator.py`
- Create: `tests/test_generator.py`

**Step 1: Write the failing test**

Create `tests/test_generator.py`:

```python
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
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_generator.py -v`

Expected: FAIL with "ModuleNotFoundError: No module named 'dnd_treasure.core.generator'"

**Step 3: Write minimal implementation**

Create `dnd_treasure/core/generator.py`:

```python
"""Main treasure generation orchestrator."""

from pathlib import Path
from typing import List, Optional

from dnd_treasure.core.dice import Dice
from dnd_treasure.core.coins import CoinGenerator
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
        """
        Generate goods for the treasure.

        For now, returns placeholder. Will be implemented in future task.
        """
        if treasure_type == TreasureType.NONE:
            return ["No Goods"]
        # TODO: Implement goods generation
        return ["No Goods"]

    def _generate_items(self, level: int, treasure_type: TreasureType) -> List[Item]:
        """
        Generate magic items for the treasure.

        For now, returns placeholder. Will be implemented in future task.
        """
        if treasure_type == TreasureType.NONE:
            return [Item(name="No Items", value=0, item_type="none")]
        # TODO: Implement item generation
        return [Item(name="No Items", value=0, item_type="none")]
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_generator.py -v`

Expected: PASS (all tests green)

**Step 5: Commit**

```bash
git add dnd_treasure/core/generator.py tests/test_generator.py
git commit -m "feat: add main treasure generator orchestrator"
```

---

## Task 10: Text Formatter

**Files:**
- Create: `dnd_treasure/formatters/base.py`
- Create: `dnd_treasure/formatters/text.py`
- Create: `tests/test_formatters.py`

**Step 1: Write the failing test**

Create `tests/test_formatters.py`:

```python
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
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_formatters.py -v`

Expected: FAIL with "ModuleNotFoundError"

**Step 3: Write minimal implementation**

Create `dnd_treasure/formatters/base.py`:

```python
"""Base formatter interface."""

from abc import ABC, abstractmethod
from dnd_treasure.core.models import Treasure


class BaseFormatter(ABC):
    """Base class for treasure formatters."""

    @abstractmethod
    def format(self, treasure: Treasure) -> str:
        """
        Format a treasure object for output.

        Args:
            treasure: The treasure to format.

        Returns:
            Formatted string representation.
        """
        pass
```

Create `dnd_treasure/formatters/text.py`:

```python
"""Human-readable text formatter."""

from dnd_treasure.core.models import Treasure
from dnd_treasure.formatters.base import BaseFormatter


class TextFormatter(BaseFormatter):
    """Formats treasure as human-readable text."""

    def format(self, treasure: Treasure) -> str:
        """
        Format treasure as readable text.

        Args:
            treasure: The treasure to format.

        Returns:
            Formatted text output.
        """
        lines = []
        lines.append(f"=== Treasure Hoard (Level {treasure.level}) ===")
        lines.append("")

        # Coins
        lines.append("COINS:")
        for coin in treasure.coins:
            lines.append(f"  {coin}")
        lines.append("")

        # Goods
        lines.append("GOODS:")
        for good in treasure.goods:
            lines.append(f"  {good}")
        lines.append("")

        # Items
        lines.append("ITEMS:")
        for item in treasure.items:
            lines.append(f"  {item.display()}")

        return "\n".join(lines)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_formatters.py -v`

Expected: PASS (all tests green)

**Step 5: Commit**

```bash
git add dnd_treasure/formatters/base.py dnd_treasure/formatters/text.py tests/test_formatters.py
git commit -m "feat: add text formatter for treasure output"
```

---

## Task 11: CLI Interface

**Files:**
- Create: `dnd_treasure/cli.py`
- Create: `tests/test_cli.py`

**Step 1: Write the failing test**

Create `tests/test_cli.py`:

```python
import pytest
from click.testing import CliRunner
from dnd_treasure.cli import main


def test_cli_basic_usage():
    """Test basic CLI usage with just level."""
    runner = CliRunner()
    result = runner.invoke(main, ['--level', '5'])

    assert result.exit_code == 0
    assert "Level 5" in result.output


def test_cli_with_treasure_types():
    """Test CLI with treasure type flags."""
    runner = CliRunner()
    result = runner.invoke(main, [
        '--level', '10',
        '--coins', 'double',
        '--goods', 'standard',
        '--items', 'triple'
    ])

    assert result.exit_code == 0
    assert "Level 10" in result.output


def test_cli_no_treasure():
    """Test CLI with all treasure disabled."""
    runner = CliRunner()
    result = runner.invoke(main, [
        '--level', '5',
        '--coins', 'none',
        '--goods', 'none',
        '--items', 'none'
    ])

    assert result.exit_code == 0
    assert "No Coins" in result.output
    assert "No Goods" in result.output


def test_cli_invalid_level():
    """Test CLI with invalid level."""
    runner = CliRunner()
    result = runner.invoke(main, ['--level', '25'])

    assert result.exit_code != 0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli.py -v`

Expected: FAIL with "ModuleNotFoundError"

**Step 3: Write minimal implementation**

Create `dnd_treasure/cli.py`:

```python
"""Command-line interface for D&D treasure generator."""

import click
from dnd_treasure.core.generator import TreasureGenerator
from dnd_treasure.core.models import TreasureType
from dnd_treasure.formatters.text import TextFormatter


TREASURE_TYPE_MAP = {
    'none': TreasureType.NONE,
    'standard': TreasureType.STANDARD,
    'double': TreasureType.DOUBLE,
    'triple': TreasureType.TRIPLE,
}


@click.command()
@click.option(
    '--level',
    '-l',
    type=click.IntRange(1, 20),
    required=True,
    help='Encounter level (1-20)'
)
@click.option(
    '--coins',
    type=click.Choice(['none', 'standard', 'double', 'triple'], case_sensitive=False),
    default='standard',
    help='Coin generation type (default: standard)'
)
@click.option(
    '--goods',
    type=click.Choice(['none', 'standard', 'double', 'triple'], case_sensitive=False),
    default='standard',
    help='Goods generation type (default: standard)'
)
@click.option(
    '--items',
    type=click.Choice(['none', 'standard', 'double', 'triple'], case_sensitive=False),
    default='standard',
    help='Items generation type (default: standard)'
)
@click.option(
    '--seed',
    type=int,
    help='Random seed for reproducible results'
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='Output file (default: stdout)'
)
def main(level, coins, goods, items, seed, output):
    """
    Generate random treasure for D&D 3.5 encounters.

    Example usage:

        dnd-treasure --level 5

        dnd-treasure --level 10 --coins double --items triple
    """
    # Create generator
    generator = TreasureGenerator(seed=seed)

    # Generate treasure
    treasure = generator.generate(
        level=level,
        coins=TREASURE_TYPE_MAP[coins.lower()],
        goods=TREASURE_TYPE_MAP[goods.lower()],
        items=TREASURE_TYPE_MAP[items.lower()],
    )

    # Format output
    formatter = TextFormatter()
    output_text = formatter.format(treasure)

    # Write output
    if output:
        with open(output, 'w') as f:
            f.write(output_text)
        click.echo(f"Treasure written to {output}")
    else:
        click.echo(output_text)


if __name__ == '__main__':
    main()
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_cli.py -v`

Expected: PASS (all tests green)

**Step 5: Commit**

```bash
git add dnd_treasure/cli.py tests/test_cli.py
git commit -m "feat: add CLI interface with click"
```

---

## Task 12: Installation & Manual Testing

**Files:**
- Modify: `README.md`

**Step 1: Install package in development mode**

Run: `pip install -e .`

Expected: Package installs successfully

**Step 2: Test CLI command**

Run: `dnd-treasure --level 5`

Expected: Outputs treasure for level 5 encounter

**Step 3: Update README with usage instructions**

Create `README.md`:

```markdown
# D&D 3.5 Treasure Generator

Python CLI tool for generating random treasure hoards for Dungeons & Dragons 3.5 edition.

## Installation

```bash
pip install -e .
```

## Usage

Generate treasure for a level 5 encounter:

```bash
dnd-treasure --level 5
```

Customize treasure types:

```bash
dnd-treasure --level 10 --coins double --items triple
```

Save output to file:

```bash
dnd-treasure --level 15 --output treasure.txt
```

Options:
- `--level, -l`: Encounter level (1-20) [required]
- `--coins`: Coin generation (none/standard/double/triple) [default: standard]
- `--goods`: Goods generation (none/standard/double/triple) [default: standard]
- `--items`: Items generation (none/standard/double/triple) [default: standard]
- `--seed`: Random seed for reproducible results
- `--output, -o`: Output file path

## Development

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=dnd_treasure tests/
```

## Project Structure

```
dnd_treasure/
├── core/          # Core generation logic
├── data/          # YAML chart files
└── formatters/    # Output formatters
```

## TODO

- [ ] Convert remaining DMG charts to YAML
- [ ] Implement goods generation
- [ ] Implement magic item generation
- [ ] Add EPH (Expanded Psionics) support
- [ ] Add MIC (Magic Item Compendium) support
- [ ] Add JSON output format
- [ ] Create Claude Code skill for treasure generation

## License

MIT
```

**Step 4: Run full test suite**

Run: `pytest -v`

Expected: All tests pass

**Step 5: Commit**

```bash
git add README.md
git commit -m "docs: add README with installation and usage instructions"
```

---

## Next Steps (Future Tasks)

The following tasks extend the core functionality but are not required for the initial release:

1. **Convert all DMG charts to YAML** - Complete conversion of remaining .txt files
2. **Implement goods generation** - Add logic for gems, art objects, etc.
3. **Implement magic item generation** - Add full DMG magic item tables
4. **Add JSON formatter** - Enable `--format json` for structured output
5. **Create Claude Code skill** - Package as a skill for use in sessions
6. **Add EPH support** - Psionic items from Expanded Psionics Handbook
7. **Add MIC support** - Items from Magic Item Compendium
8. **Multi-source percentage** - Implement the VB multi-source feature

---

## Testing Checklist

Before considering this complete:

- [ ] All unit tests pass
- [ ] CLI can generate treasure for levels 1-20
- [ ] Coin generation produces valid output
- [ ] Output format is readable
- [ ] Package installs correctly
- [ ] README is accurate and complete
