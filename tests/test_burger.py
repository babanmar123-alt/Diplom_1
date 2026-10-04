import pytest
from unittest.mock import MagicMock
from praktikum.burger import Burger


class TestBurgerInit:
    def test_init_bun_is_none(self):
        burger = Burger()
        assert burger.bun is None

    def test_init_ingredients_is_empty(self):
        burger = Burger()
        assert burger.ingredients == []


class TestSetBuns:
    def test_set_buns(self, mock_bun):
        burger = Burger()
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_set_buns_twice(self, mock_bun):
        burger = Burger()
        burger.set_buns(mock_bun)
        new_bun = MagicMock()
        burger.set_buns(new_bun)
        assert burger.bun == new_bun


class TestAddIngredient:
    def test_add_one_ingredient(self, mock_ingredient_sauce):
        burger = Burger()
        burger.add_ingredient(mock_ingredient_sauce)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient_sauce

    @pytest.mark.parametrize("count", [1, 2, 3, 5])
    def test_add_multiple_ingredients(self, count):
        burger = Burger()
        for _ in range(count):
            burger.add_ingredient(MagicMock())
        assert len(burger.ingredients) == count

    def test_add_sauce_and_filling(self, mock_ingredient_sauce, mock_ingredient_filling):
        burger = Burger()
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)
        assert len(burger.ingredients) == 2


class TestRemoveIngredient:
    def test_remove_ingredient(self, mock_ingredient_sauce):
        burger = Burger()
        burger.add_ingredient(mock_ingredient_sauce)
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 0

    def test_remove_first_of_two(self):
        burger = Burger()
        ing1, ing2 = MagicMock(), MagicMock()
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)
        burger.remove_ingredient(0)
        assert burger.ingredients == [ing2]

    def test_remove_second_of_two(self):
        burger = Burger()
        ing1, ing2 = MagicMock(), MagicMock()
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)
        burger.remove_ingredient(1)
        assert burger.ingredients == [ing1]

    def test_remove_from_empty_raises_index_error(self):
        burger = Burger()
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)

    def test_remove_invalid_index_raises_index_error(self, mock_ingredient_sauce):
        burger = Burger()
        burger.add_ingredient(mock_ingredient_sauce)
        with pytest.raises(IndexError):
            burger.remove_ingredient(5)


class TestMoveIngredient:
    def test_move_ingredient_forward(self):
        burger = Burger()
        ing1, ing2, ing3 = MagicMock(), MagicMock(), MagicMock()
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)
        burger.add_ingredient(ing3)
        burger.move_ingredient(0, 2)
        assert burger.ingredients == [ing2, ing3, ing1]

    def test_move_ingredient_backward(self):
        burger = Burger()
        ing1, ing2, ing3 = MagicMock(), MagicMock(), MagicMock()
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)
        burger.add_ingredient(ing3)
        burger.move_ingredient(2, 0)
        assert burger.ingredients == [ing3, ing1, ing2]

    def test_move_ingredient_same_position(self):
        burger = Burger()
        ing1, ing2 = MagicMock(), MagicMock()
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)
        burger.move_ingredient(0, 0)
        assert burger.ingredients == [ing1, ing2]

    @pytest.mark.parametrize("index,new_index,expected_order", [
        (0, 1, [1, 0, 2]),
        (1, 2, [0, 2, 1]),
        (2, 1, [0, 2, 1]),
    ])
    def test_move_ingredient_parametrized(self, index, new_index, expected_order):
        burger = Burger()
        ingredients = [MagicMock(), MagicMock(), MagicMock()]
        for ing in ingredients:
            burger.add_ingredient(ing)
        burger.move_ingredient(index, new_index)
        expected = [ingredients[i] for i in expected_order]
        assert burger.ingredients == expected


class TestGetPrice:
    def test_get_price_only_bun(self, mock_bun):
        burger = Burger()
        burger.set_buns(mock_bun)
        assert burger.get_price() == 200.0

    def test_get_price_with_one_ingredient(self, mock_bun, mock_ingredient_sauce):
        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)
        assert burger.get_price() == 300.0

    def test_get_price_with_sauce_and_filling(self, mock_bun, mock_ingredient_sauce, mock_ingredient_filling):
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
        burger = Burger()
        burger.set_buns(mock_bun)
        for price in ingredient_prices:
            ing = MagicMock()
            ing.get_price.return_value = price
            burger.add_ingredient(ing)
        assert burger.get_price() == expected_price


class TestGetReceipt:
    def test_get_receipt_only_bun(self, mock_bun):
        burger = Burger()
        burger.set_buns(mock_bun)
        receipt = burger.get_receipt()
        assert "(==== black bun ====)" in receipt
        assert "Price: 200.0" in receipt

    def test_get_receipt_with_sauce(self, mock_bun, mock_ingredient_sauce):
        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)
        receipt = burger.get_receipt()
        assert "(==== black bun ====)" in receipt
        assert "= sauce hot sauce =" in receipt
        assert "Price: 300.0" in receipt

    def test_get_receipt_with_filling(self, mock_bun, mock_ingredient_filling):
        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_filling)
        receipt = burger.get_receipt()
        assert "= filling cutlet =" in receipt

    def test_get_receipt_lowercase_type(self, mock_bun):
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
        burger = Burger()
        burger.set_buns(mock_bun)
        receipt = burger.get_receipt()
        assert receipt.startswith("(==== black bun ====)")

    def test_get_receipt_ends_with_price(self, mock_bun):
        burger = Burger()
        burger.set_buns(mock_bun)
        receipt = burger.get_receipt()
        assert receipt.endswith("Price: 200.0")