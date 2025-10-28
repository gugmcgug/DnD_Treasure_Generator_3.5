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
