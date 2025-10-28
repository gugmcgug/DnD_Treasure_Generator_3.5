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
