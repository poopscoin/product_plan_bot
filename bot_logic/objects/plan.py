from datetime import datetime
from .product import ProductBuilder, Product, ProductType

class Plan:
    def __init__(self, *, product_list: dict[int, Product] = None, title : str = None):
        self._title = title or "New plan - " + datetime.today().strftime("%d.%m.%y")
        self._product_list = product_list or {}
        self._product_count = len(self.product_list)
        self._making_product = ProductBuilder()

    def add_product(self, *, product: Product) -> None:
        new_id = max(self._product_list.keys(), default=0) + 1
        self._product_list[new_id] = product
    
    def build_new_product(self, *, step: str, value: str|int|float|ProductType) -> bool|Product:
        finished, new_builder = self._making_product.build(step=step, value=value)
        if finished:
            self.add_product(product=finished)
            self._making_product = new_builder
        return finished
    
    def build_crash(self):
        self._making_product = ProductBuilder()
    
    @property
    def products(self) -> dict[int, Product]:
        return self._product_list
        

