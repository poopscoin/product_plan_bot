from dataclasses import dataclass
from mlangm import translate as _
import re

def get_count_and_type(value: str) -> tuple[float, str]:
    find_number = re.search(r"^\d+(?:[.,]?\d*)?", value.strip())
    if not find_number:
        return 0, ""

    type = value[len(find_number.group(0)):].strip()
    number_for_corect = find_number.group(0).replace(",", ".")

    return float(number_for_corect), type

def complete_values_writer(value_name: str):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            if args and isinstance(args[0], dict):
                self._complete_values.setdefault(value_name, {}).update(args[0])
            else:
                self._complete_values[value_name] = args[0] if args else kwargs.get(func.__name__)
        return wrapper
    return decorator

@dataclass
class Product:
    name: str = None
    count: int|float = None
    type: str = None
    storages_price: dict[str:int] = None

class ProductBuilder:

    NAME = 'write_name'
    COUNT = 'write_count'
    
    COMPLETE = 'complete'

    def __init__(self):
        self._product = Product()
        self._complete_values = {}

    @property
    def product(self) -> Product:
        return self._product

    @property
    def store_price(self):
        return self._product.storage_price

    @store_price.setter
    @complete_values_writer('product_store_price')
    def store_price(self, store_price: dict[str:int]):
        self._product.store_price += store_price

    @property
    def values(self):
        return self._complete_values

    @property
    def name(self):
        return self._product.name

    @name.setter
    @complete_values_writer('product_name')
    def name(self, name: str|None):
        self._product.name = name

    @property
    def count(self):
        return self._product.count

    @count.setter
    @complete_values_writer('product_count')
    def count(self, count: int|float|None):
        self._product.count = count

    @property
    def type(self):
        return self._product.type

    @type.setter
    @complete_values_writer('product_type')
    def type(self, type: str|None):
        self._product.type = type

    def get(self, value: str):
        match value:
            case self.NAME:
                return self.name
            case self.COUNT:
                return str(self.count) + self.type

    def next(self):
        if self._product.name == None:
            return self.NAME
        elif self._product.count == None:
            return self.COUNT
        else:
            return self.COMPLETE

    def step_back(self):
        if self.count:
            self.count = None
            self.type = None
            return self.COUNT
        elif self.name:
            self.name = None
            return self.NAME

    def build(self, value: str|int|float) -> tuple[str | Product, dict]:
        if not self.name:
            self.name = value
            info = self.COUNT
        elif not self._product.count:
            self.count, self.type = get_count_and_type(value)
            info = self.COMPLETE
        else:
            info = self.COMPLETE
        return info, self._complete_values