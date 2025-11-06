"""Convert VB chart files to YAML format."""

import yaml
from pathlib import Path


def parse_chart_file(file_path: Path) -> dict:
    """Parse a VB chart .txt file into a dictionary."""
    # Try UTF-8 first, fall back to latin-1 for files with special characters
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            all_lines = [line.strip() for line in f if line.strip()]
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
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
        # Already converted
        # ("DMGArmor.txt", "armor.yaml", "DMG Armor Types"),
        # ("DMGPotionsMin.txt", "potions_minor.yaml", "DMG Minor Potions"),
        # ("DMGAlignments.txt", "alignments.yaml", "DMG Alignments"),

        # Keyword reference charts
        ("DMGEnergy.txt", "energy.yaml", "DMG Energy Types"),
        ("DMGBaneCreatureType.txt", "bane_creature_type.yaml", "DMG Bane Creature Types"),

        # Potion charts
        ("DMGPotionsMed.txt", "potions_medium.yaml", "DMG Medium Potions"),
        ("DMGPotionsMaj.txt", "potions_major.yaml", "DMG Major Potions"),

        # Weapon charts
        ("DMGComMeleeWeapons.txt", "common_melee_weapons.yaml", "DMG Common Melee Weapons"),
        ("DMGUncMeleeWeapons.txt", "uncommon_melee_weapons.yaml", "DMG Uncommon Melee Weapons"),
        ("DMGRangedWeapons.txt", "ranged_weapons.yaml", "DMG Ranged Weapons"),
        ("DMGMeleeWepMin.txt", "melee_weapon_minor.yaml", "DMG Minor Magic Melee Weapons"),
        ("DMGMeleeWepMed.txt", "melee_weapon_medium.yaml", "DMG Medium Magic Melee Weapons"),
        ("DMGMeleeWepMaj.txt", "melee_weapon_major.yaml", "DMG Major Magic Melee Weapons"),
        ("DMGRangedWepMin.txt", "ranged_weapon_minor.yaml", "DMG Minor Magic Ranged Weapons"),
        ("DMGRangedWepMed.txt", "ranged_weapon_medium.yaml", "DMG Medium Magic Ranged Weapons"),
        ("DMGRangedWepMaj.txt", "ranged_weapon_major.yaml", "DMG Major Magic Ranged Weapons"),
        ("DMGWepSpecificMin.txt", "weapon_specific_minor.yaml", "DMG Minor Specific Weapons"),
        ("DMGWepSpecificMed.txt", "weapon_specific_medium.yaml", "DMG Medium Specific Weapons"),
        ("DMGWepSpecificMaj.txt", "weapon_specific_major.yaml", "DMG Major Specific Weapons"),

        # Armor charts
        ("DMGArmorMin.txt", "armor_minor.yaml", "DMG Minor Magic Armor"),
        ("DMGArmorMed.txt", "armor_medium.yaml", "DMG Medium Magic Armor"),
        ("DMGArmorMaj.txt", "armor_major.yaml", "DMG Major Magic Armor"),
        ("DMGArmorSpecificMin.txt", "armor_specific_minor.yaml", "DMG Minor Specific Armor"),
        ("DMGArmorSpecificMed.txt", "armor_specific_medium.yaml", "DMG Medium Specific Armor"),
        ("DMGArmorSpecificMaj.txt", "armor_specific_major.yaml", "DMG Major Specific Armor"),

        # Shield charts
        ("DMGShields.txt", "shields.yaml", "DMG Shields"),
        ("DMGShieldMin.txt", "shield_minor.yaml", "DMG Minor Magic Shields"),
        ("DMGShieldMed.txt", "shield_medium.yaml", "DMG Medium Magic Shields"),
        ("DMGShieldMaj.txt", "shield_major.yaml", "DMG Major Magic Shields"),
        ("DMGShieldSpecificMin.txt", "shield_specific_minor.yaml", "DMG Minor Specific Shields"),
        ("DMGShieldSpecificMed.txt", "shield_specific_medium.yaml", "DMG Medium Specific Shields"),
        ("DMGShieldSpecificMaj.txt", "shield_specific_major.yaml", "DMG Major Specific Shields"),

        # Rings
        ("DMGRingsMin.txt", "rings_minor.yaml", "DMG Minor Rings"),
        ("DMGRingsMed.txt", "rings_medium.yaml", "DMG Medium Rings"),
        ("DMGRingsMaj.txt", "rings_major.yaml", "DMG Major Rings"),

        # Rods
        ("DMGRodsMed.txt", "rods_medium.yaml", "DMG Medium Rods"),
        ("DMGRodsMaj.txt", "rods_major.yaml", "DMG Major Rods"),

        # Staffs
        ("DMGStaffsMed.txt", "staffs_medium.yaml", "DMG Medium Staffs"),
        ("DMGStaffsMaj.txt", "staffs_major.yaml", "DMG Major Staffs"),

        # Wands
        ("DMGWandsMin.txt", "wands_minor.yaml", "DMG Minor Wands"),
        ("DMGWandsMed.txt", "wands_medium.yaml", "DMG Medium Wands"),
        ("DMGWandsMaj.txt", "wands_major.yaml", "DMG Major Wands"),

        # Wonderous Items
        ("DMGWonderousMin.txt", "wonderous_minor.yaml", "DMG Minor Wonderous Items"),
        ("DMGWonderousMed.txt", "wonderous_medium.yaml", "DMG Medium Wonderous Items"),
        ("DMGWonderousMaj.txt", "wonderous_major.yaml", "DMG Major Wonderous Items"),
    ]

    for input_file, output_file, name in conversions:
        try:
            convert_chart(
                charts_base / input_file,
                output_base / output_file,
                name
            )
        except Exception as e:
            print(f"Error converting {input_file}: {e}")
