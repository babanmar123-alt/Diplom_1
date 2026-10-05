from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestIngredient:
    def test_get_type_sauce(self):
        ing = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        assert ing.get_type() == INGREDIENT_TYPE_SAUCE

    def test_get_type_filling(self):
        ing = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 200)
        assert ing.get_type() == INGREDIENT_TYPE_FILLING

    def test_get_name(self):
        ing = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        assert ing.get_name() == "hot sauce"

    def test_get_price(self):
        ing = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        assert ing.get_price() == 100

    def test_init_attributes(self):
        ing = Ingredient("FILLING", "cutlet", 200)
        assert ing.type == "FILLING"
        assert ing.name == "cutlet"
        assert ing.price == 200