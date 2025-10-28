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
