from enum import Enum
from dataclasses import dataclass

class ProductType(Enum):
    LIQUID = ["мл.", "л."]
    WEIGHT = ["г.", "кг."]
    PIECE = ["шт."]

    def units(self) -> list[str]:
        return self.value

@dataclass
class Product:
    name: str = None
    count: int = 0
    type: ProductType|str = None

class ProductBuilder:
    def __init__(self):
        self._product: Product | None = None

    def set_name(self, *, name: str):
        self._product.name = name

    def set_count(self, *, count: int):
        self._product.count = count

    def set_type(self, *, type_product: ProductType|str):
        self._product.type = type_product

    def is_ready(self) -> bool:
        return all([self._product.name, self._product.count is not None, self._product.type])

    def build(self, *, step: str, value: str|int|float|ProductType) -> tuple[bool | Product, 'ProductBuilder'] | bool:
        if step == "name":
            self.set_name(name=value)
        elif step == "count":
            self.set_count(count=value)
        elif step == "type":
            self.set_type(type_product=value)
        
        if self.is_ready():
            product = Product()
            product.name = self._name
            product.count = self._count
            product.type = self._type
            return product, ProductBuilder()
        return False