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
