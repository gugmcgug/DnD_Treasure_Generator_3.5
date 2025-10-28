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
