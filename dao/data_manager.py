import json

from models.product import Product, ProductList
from models.member import Member, MemberList
from models.order import Order, OrderList


class DataManager:
    FILE_NAME = "data.json"

    @staticmethod
    def save_data():
        data = {
            "products": [
                product.to_dict()
                for product in ProductList.product_list
            ],
            "members": [
                member.to_dict()
                for member in MemberList.member_list
            ],
            "orders": [
                order.to_dict()
                for order in OrderList.order_list
            ]
        }

        with open(DataManager.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

    @staticmethod
    def load_data():
        try:
            with open(DataManager.FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 防止重复加载
            ProductList.product_list.clear()
            MemberList.member_list.clear()
            OrderList.order_list.clear()

            # 商品
            for item in data.get("products", []):
                product = Product.from_dict(item)
                ProductList.product_list.append(product)

            # 会员
            for item in data.get("members", []):
                member = Member.from_dict(item)
                MemberList.member_list.append(member)

            # 订单
            for item in data.get("orders", []):
                order = Order.from_dict(item)
                OrderList.order_list.append(order)

            print("数据加载成功！")

        except FileNotFoundError:
            print("第一次运行，创建数据文件！")
            DataManager.create_file()

    @staticmethod
    def create_file():
        data = {
            "products": [],
            "members": [],
            "orders": []
        }

        with open(DataManager.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )
