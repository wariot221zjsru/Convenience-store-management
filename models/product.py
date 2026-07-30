# 商品类
class Product:

    def __init__(self, id, name, price, stock, category):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category

    # 修改商品ID
    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    # 修改商品名称
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    # 修改商品价格
    def set_price(self, price):
        self.price = price

    def get_price(self):
        return self.price

    # 修改商品库存
    def set_stock(self, stock):
        self.stock = stock

    def get_stock(self):
        return self.stock

    # 修改商品分类
    def set_category(self, category):
        self.category = category

    def get_category(self):
        return self.category

    # 对象转换成字典
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category": self.category
        }

    # 字典转换成对象
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["name"],
            data["price"],
            data["stock"],
            data["category"]
        )


# 商品列表
class ProductList:
    product_list = []
