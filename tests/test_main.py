import pytest
from main import Game


def test_game_update():
    """Test one update cycle."""
    game = Game()
    old_time = game.delta_time
    game.update()
    assert game.delta_time != old_time
