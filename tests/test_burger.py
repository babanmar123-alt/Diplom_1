import pytest
from unittest.mock import MagicMock
from praktikum.burger import Burger


class TestSetBuns:
    """Тесты метода set_buns."""

    def test_set_buns_changes_price(self):
        """После установки булочки цена считается по её цене."""
        burger = Burger()
        bun = MagicMock()
        bun.get_price.return_value = 100.0
        bun.get_name.return_value = "black bun"

        burger.set_buns(bun)

        assert burger.get_price() == 200.0

    def test_set_buns_twice_uses_last_bun(self):
        """Повторная установка булочки перезаписывает предыдущую."""
        burger = Burger()
        first_bun = MagicMock()
        first_bun.get_price.return_value = 100.0
        second_bun = MagicMock()
        second_bun.get_price.return_value = 300.0

        burger.set_buns(first_bun)
        burger.set_buns(second_bun)

        assert burger.get_price() == 600.0


class TestAddIngredient:
    """Тесты метода add_ingredient."""

    def test_add_one_ingredient_changes_price(self, mock_bun):
        """После добавления ингредиента цена увеличивается."""
        burger = Burger()
        burger.set_buns(mock_bun)

        ingredient = MagicMock()
        ingredient.get_price.return_value = 100.0

        burger.add_ingredient(ingredient)

        assert burger.get_price() == 300.0

    @pytest.mark.parametrize("count", [1, 2, 3, 5])
    def test_add_multiple_ingredients_changes_price(self, mock_bun, count):
        """После добавления нескольких ингредиентов цена суммируется."""
        burger = Burger()
        burger.set_buns(mock_bun)

        for _ in range(count):
            ingredient = MagicMock()
            ingredient.get_price.return_value = 50.0
            burger.add_ingredient(ingredient)

        assert burger.get_price() == 200.0 + 50.0 * count

    def test_add_sauce_and_filling(self, mock_bun, mock_ingredient_sauce, mock_ingredient_filling):
        """После добавления соуса и начинки цена суммируется."""
        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)

        assert burger.get_price() == 500.0


class TestRemoveIngredient:
    """Тесты метода remove_ingredient."""

    def test_remove_ingredient_decreases_price(self, mock_bun, mock_ingredient_sauce):
        """После удаления ингредиента цена уменьшается."""
        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)

        burger.remove_ingredient(0)

        assert burger.get_price() == 200.0

    def test_remove_first_of_two_decreases_price(self, mock_bun):
        """При удалении первого из двух ингредиентов цена уменьшается на его стоимость."""
        burger = Burger()
        burger.set_buns(mock_bun)

        ing1 = MagicMock()
        ing1.get_price.return_value = 100.0
        ing2 = MagicMock()
        ing2.get_price.return_value = 200.0

        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)

        burger.remove_ingredient(0)

        assert burger.get_price() == 400.0

    def test_remove_second_of_two_decreases_price(self, mock_bun):
        """При удалении второго из двух ингредиентов цена уменьшается на его стоимость."""
        burger = Burger()
        burger.set_buns(mock_bun)

        ing1 = MagicMock()
        ing1.get_price.return_value = 100.0
        ing2 = MagicMock()
        ing2.get_price.return_value = 200.0

        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)

        burger.remove_ingredient(1)

        assert burger.get_price() == 300.0

    def test_remove_from_empty_raises_index_error(self):
        """Удаление из пустого бургера вызывает IndexError."""
        burger = Burger()
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)

    def test_remove_invalid_index_raises_index_error(self, mock_bun):
        """Удаление по несуществующему индексу вызывает IndexError."""
        burger = Burger()
        burger.set_buns(mock_bun)
        ingredient = MagicMock()
        ingredient.get_price.return_value = 100.0
        burger.add_ingredient(ingredient)

        with pytest.raises(IndexError):
            burger.remove_ingredient(5)


class TestMoveIngredient:
    """Тесты метода move_ingredient."""

    def test_move_ingredient_changes_receipt_order(self, mock_bun):
        """После перемещения ингредиента меняется порядок в чеке."""
        burger = Burger()
        burger.set_buns(mock_bun)

        ing1 = MagicMock()
        ing1.get_type.return_value = "SAUCE"
        ing1.get_name.return_value = "hot sauce"
        ing1.get_price.return_value = 100.0

        ing2 = MagicMock()
        ing2.get_type.return_value = "FILLING"
        ing2.get_name.return_value = "cutlet"
        ing2.get_price.return_value = 200.0

        ing3 = MagicMock()
        ing3.get_type.return_value = "SAUCE"
        ing3.get_name.return_value = "chili"
        ing3.get_price.return_value = 300.0

        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)
        burger.add_ingredient(ing3)

        burger.move_ingredient(0, 2)

        receipt = burger.get_receipt()

        assert receipt.index("cutlet") < receipt.index("chili")
        assert receipt.index("chili") < receipt.index("hot sauce")

    @pytest.mark.parametrize("index,new_index,first_after", [
        (0, 1, "cutlet"),
        (1, 2, "hot sauce"),
        (2, 1, "hot sauce"),
    ])
    def test_move_ingredient_parametrized(self, mock_bun, index, new_index, first_after):
        """Параметризованная проверка перемещения ингредиентов."""
        burger = Burger()
        burger.set_buns(mock_bun)

        ingredients = []
        for name in ["hot sauce", "cutlet", "chili"]:
            ing = MagicMock()
            ing.get_type.return_value = "SAUCE"
            ing.get_name.return_value = name
            ing.get_price.return_value = 100.0
            ingredients.append(ing)
            burger.add_ingredient(ing)

        burger.move_ingredient(index, new_index)

        receipt = burger.get_receipt()
        first_line = receipt.split("\n")[1]
        first_ingredient_name = first_line.replace("= sauce ", "").replace(" =", "")
        assert first_ingredient_name == first_after


class TestGetPrice:
    """Тесты метода get_price."""

    def test_get_price_only_bun(self, mock_bun):
        """Цена только с булочкой — булочка × 2."""
        burger = Burger()
        burger.set_buns(mock_bun)

        assert burger.get_price() == 200.0

    def test_get_price_with_one_ingredient(self, mock_bun, mock_ingredient_sauce):
        """Цена с булочкой и одним ингредиентом."""
        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)

        assert burger.get_price() == 300.0

    def test_get_price_with_sauce_and_filling(self, mock_bun, mock_ingredient_sauce, mock_ingredient_filling):
        """Цена с булочкой, соусом и начинкой."""
        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)

        assert burger.get_price() == 500.0

    @pytest.mark.parametrize("ingredient_prices,expected_price", [
        ([], 200.0),
        ([100.0], 300.0),
        ([100.0, 200.0], 500.0),
        ([100.0, 200.0, 300.0], 800.0),
    ])
    def test_get_price_parametrized(self, mock_bun, ingredient_prices, expected_price):
        """Параметризованная проверка цены."""
        burger = Burger()
        burger.set_buns(mock_bun)
        for price in ingredient_prices:
            ing = MagicMock()
            ing.get_price.return_value = price
            burger.add_ingredient(ing)

        assert burger.get_price() == expected_price


class TestGetReceipt:
    """Тесты метода get_receipt."""

    def test_get_receipt_only_bun(self, mock_bun):
        """Чек содержит название булочки и цену."""
        burger = Burger()
        burger.set_buns(mock_bun)

        receipt = burger.get_receipt()

        assert "(==== black bun ====)" in receipt
        assert "Price: 200.0" in receipt

    def test_get_receipt_with_sauce(self, mock_bun, mock_ingredient_sauce):
        """Чек содержит соус в нижнем регистре."""
        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)

        receipt = burger.get_receipt()

        assert "= sauce hot sauce =" in receipt
        assert "Price: 300.0" in receipt

    def test_get_receipt_with_filling(self, mock_bun, mock_ingredient_filling):
        """Чек содержит начинку в нижнем регистре."""
        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_filling)

        receipt = burger.get_receipt()

        assert "= filling cutlet =" in receipt

    def test_get_receipt_lowercase_type(self, mock_bun):
        """Тип ингредиента отображается в нижнем регистре."""
        burger = Burger()
        burger.set_buns(mock_bun)

        ing = MagicMock()
        ing.get_type.return_value = "SAUCE"
        ing.get_name.return_value = "hot sauce"
        ing.get_price.return_value = 100.0
        burger.add_ingredient(ing)

        receipt = burger.get_receipt()

        assert "= sauce hot sauce =" in receipt

    def test_get_receipt_starts_with_bun(self, mock_bun):
        """Чек начинается с булочки."""
        burger = Burger()
        burger.set_buns(mock_bun)

        receipt = burger.get_receipt()

        assert receipt.startswith("(==== black bun ====)")

    def test_get_receipt_ends_with_price(self, mock_bun):
        """Чек заканчивается ценой."""
        burger = Burger()
        burger.set_buns(mock_bun)

        receipt = burger.get_receipt()

        assert receipt.endswith("Price: 200.0")