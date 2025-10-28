import pytest
from click.testing import CliRunner
from dnd_treasure.cli import main


def test_cli_basic_usage():
    """Test basic CLI usage with just level."""
    runner = CliRunner()
    result = runner.invoke(main, ['--level', '5'])

    assert result.exit_code == 0
    assert "Level 5" in result.output


def test_cli_with_treasure_types():
    """Test CLI with treasure type flags."""
    runner = CliRunner()
    result = runner.invoke(main, [
        '--level', '10',
        '--coins', 'double',
        '--goods', 'standard',
        '--items', 'triple'
    ])

    assert result.exit_code == 0
    assert "Level 10" in result.output


def test_cli_no_treasure():
    """Test CLI with all treasure disabled."""
    runner = CliRunner()
    result = runner.invoke(main, [
        '--level', '5',
        '--coins', 'none',
        '--goods', 'none',
        '--items', 'none'
    ])

    assert result.exit_code == 0
    assert "No Coins" in result.output
    assert "No Goods" in result.output


def test_cli_invalid_level():
    """Test CLI with invalid level."""
    runner = CliRunner()
    result = runner.invoke(main, ['--level', '25'])

    assert result.exit_code != 0
