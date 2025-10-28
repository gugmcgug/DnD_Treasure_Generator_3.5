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
