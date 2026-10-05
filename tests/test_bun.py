from praktikum.bun import Bun


class TestBun:
    def test_get_name(self):
        bun = Bun("black bun", 100)
        assert bun.get_name() == "black bun"

    def test_get_price(self):
        bun = Bun("black bun", 100)
        assert bun.get_price() == 100

    def test_init_attributes(self):
        bun = Bun("white bun", 200)
        assert bun.name == "white bun"
        assert bun.price == 200

    def test_get_name_returns_str(self):
        bun = Bun("red bun", 300)
        assert isinstance(bun.get_name(), str)

    def test_get_price_returns_float(self):
        bun = Bun("red bun", 300.5)
        assert bun.get_price() == 300.5