from praktikum.database import Database
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient


class TestDatabase:
    def test_init_buns_count(self):
        db = Database()
        assert len(db.buns) == 3

    def test_init_ingredients_count(self):
        db = Database()
        assert len(db.ingredients) == 6

    def test_available_buns_returns_list(self):
        db = Database()
        buns = db.available_buns()
        assert isinstance(buns, list)
        assert len(buns) == 3

    def test_available_ingredients_returns_list(self):
        db = Database()
        ingredients = db.available_ingredients()
        assert isinstance(ingredients, list)
        assert len(ingredients) == 6

    def test_available_buns_contains_bun_objects(self):
        db = Database()
        buns = db.available_buns()
        for bun in buns:
            assert isinstance(bun, Bun)

    def test_available_ingredients_contains_ingredient_objects(self):
        db = Database()
        ingredients = db.available_ingredients()
        for ing in ingredients:
            assert isinstance(ing, Ingredient)

    def test_database_returns_same_list(self):
        db = Database()
        assert db.available_buns() is db.buns
        assert db.available_ingredients() is db.ingredients