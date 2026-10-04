import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_bun():
    """Мок булочки с фиксированными значениями."""
    bun = MagicMock()
    bun.get_name.return_value = "black bun"
    bun.get_price.return_value = 100.0
    return bun


@pytest.fixture
def mock_ingredient_sauce():
    """Мок соуса."""
    ingredient = MagicMock()
    ingredient.get_type.return_value = "SAUCE"
    ingredient.get_name.return_value = "hot sauce"
    ingredient.get_price.return_value = 100.0
    return ingredient


@pytest.fixture
def mock_ingredient_filling():
    """Мок начинки."""
    ingredient = MagicMock()
    ingredient.get_type.return_value = "FILLING"
    ingredient.get_name.return_value = "cutlet"
    ingredient.get_price.return_value = 200.0
    return ingredient