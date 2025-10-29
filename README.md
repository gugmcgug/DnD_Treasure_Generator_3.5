# D&D 3.5 Treasure Generator

Python CLI tool for generating random treasure hoards for Dungeons & Dragons 3.5 edition.

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for Python package management.

Install in development mode:

```bash
uv pip install -e .
```

This will install the `dnd-treasure` command and all dependencies.

## Usage

Generate treasure for a level 5 encounter:

```bash
python3 -m dnd_treasure.cli --level 5
```

Customize treasure types:

```bash
python3 -m dnd_treasure.cli --level 10 --coins double --items triple
```

Save output to file:

```bash
python3 -m dnd_treasure.cli --level 15 --output treasure.txt
```

Use a seed for reproducible results:

```bash
python3 -m dnd_treasure.cli --level 7 --seed 12345
```

## Options

- `--level, -l`: Encounter level (1-20) **[required]**
- `--coins`: Coin generation type (none/standard/double/triple) [default: standard]
- `--goods`: Goods generation type (none/standard/double/triple) [default: standard]
- `--items`: Items generation type (none/standard/double/triple) [default: standard]
- `--seed`: Random seed for reproducible results
- `--output, -o`: Output file path (default: stdout)

## Development

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=dnd_treasure tests/
```

Run tests in verbose mode:

```bash
pytest -v
```

## Project Structure

```
dnd_treasure/
├── core/          # Core generation logic (dice, coins, models, generator, keywords)
├── data/          # YAML chart files and data loader
│   └── charts/
│       └── dmg/   # Dungeon Master's Guide charts
└── formatters/    # Output formatters (text, base)
```

## Features

- **Table-driven generation**: Uses YAML data files for extensibility
- **DMG coin generation**: Implements standard D&D 3.5 treasure tables
- **Keyword substitution**: Dynamic item names with {alignment}, {energy}, etc.
- **Flexible treasure types**: None/standard/double/triple for coins, goods, and items
- **Reproducible results**: Optional seed parameter for testing
- **Clean architecture**: Modular design separating concerns

## TODO

- [ ] Convert remaining DMG charts to YAML
- [ ] Implement goods generation (gems, art objects)
- [ ] Implement magic item generation (armor, weapons, potions, etc.)
- [ ] Add EPH (Expanded Psionics Handbook) support
- [ ] Add MIC (Magic Item Compendium) support
- [ ] Add JSON output format
- [ ] Create Claude Code skill for treasure generation

## License

MIT

---

## Legacy Version

The original VB.NET version is in the `Treasure_Generator/` directory. This Python rewrite provides:
- Modern CLI interface
- Cross-platform compatibility
- Extensible YAML-based data format
- Comprehensive test coverage
- Cleaner, more maintainable architecture
