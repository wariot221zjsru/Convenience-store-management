# 订单明细类
class OrderItem:

    def __init__(self, product_id, product_name, price, quantity):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.quantity = quantity

    # 商品小计
    @property
    def subtotal(self):
        return self.price * self.quantity

    # 对象转换成字典
    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "price": self.price,
            "quantity": self.quantity
        }

    # 字典转换成对象
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["product_id"],
            data["product_name"],
            data["price"],
            data["quantity"]
        )


# 订单类
class Order:

    def __init__(self, order_id, items, member_phone, member_id, total_amount, real_amount, points, pay_method, trading_hour):
        self.order_id = order_id

        # 列表存放订单明细类
        self.items = items

        self.member_phone = member_phone
        self.member_id = member_id

        # 原价
        self.total_amount = total_amount

        # 实付
        self.real_amount = real_amount

        # 获得积分
        self.points = points

        self.pay_method = pay_method
        self.trading_hour = trading_hour

    # 对象转换成字典
    def to_dict(self):
        return {
            "order_id": self.order_id,
            "items": [
                item.to_dict()
                for item in self.items
            ],
            "member_phone": self.member_phone,
            "member_id": self.member_id,
            "total_amount": self.total_amount,
            "real_amount": self.real_amount,
            "points": self.points,
            "pay_method": self.pay_method,
            "trading_hour": str(self.trading_hour)
        }

    # 字典转换成对象
    @classmethod
    def from_dict(cls, data):
        items = [
            OrderItem.from_dict(item)
            for item in data["items"]
        ]

        return cls(
            data["order_id"],
            items,
            data["member_phone"],
            data["member_id"],
            data["total_amount"],
            data["real_amount"],
            data["points"],
            data["pay_method"],
            data["trading_hour"]
        )


# 订单列表
class OrderList:
    order_list = []
