"""Convert VB chart files to YAML format."""

import yaml
from pathlib import Path


def parse_chart_file(file_path: Path) -> dict:
    """Parse a VB chart .txt file into a dictionary."""
    with open(file_path, 'r') as f:
        all_lines = [line.strip() for line in f if line.strip()]

    # Separate data lines from comment lines
    data_lines = [line for line in all_lines if not line.startswith('//')]
    comment_lines = [line for line in all_lines if line.startswith('//')]

    num_entries = int(data_lines[0])
    entries = []

    for i in range(1, num_entries + 1):
        parts = data_lines[i].split('|')
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
    source = "DMG"
    page = None
    table = None

    for line in comment_lines:
        if "Page" in line:
            # Extract numbers from "Page 216"
            import re
            match = re.search(r'Page\s+(\d+)', line)
            if match:
                page = int(match.group(1))
        if "Table" in line:
            # Extract "7-3" from "Table 7-3:Random Armor Type"
            import re
            match = re.search(r'Table\s+([\d\-]+)', line)
            if match:
                table = match.group(1)

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
