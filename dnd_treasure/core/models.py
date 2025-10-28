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
