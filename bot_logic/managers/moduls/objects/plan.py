from datetime import datetime
from mlangm import translate as _

from .products import ProductBuilder, Product

class Plan:
    def __init__(self, id: int, *, product_list: dict[int, Product] = None, title: str = None, lang: str = 'en'):
        self._id = id
        self._title = title or _('placeholders.title_plan', lang) + datetime.today().strftime("%d.%m.%y %H:%M")
        self._product_list = product_list or {}
        self._product_count = len(self._product_list)

    @property
    def title(self) -> str:
        return self._title

    @property
    def products(self) -> dict[int, Product]:
        return self._product_list

    @property
    def count(self) -> int:
        return len(self._product_list)

    @property
    def id(self) -> int:
        return self._id

    def add_product(self, product: Product) -> None:
        index = len(self._product_list)
        self._product_list[index] = product

        

