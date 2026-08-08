import json
import os
import tempfile

from models.product import Product, ProductList
from models.member import Member, MemberList
from models.order import Order, OrderList


class DataManager:
    FILE_NAME = "data.json"

    @staticmethod
    def save_data():
        """
        原子化保存数据：
        先将完整 JSON 写入一个临时文件，写入成功后再原子替换目标文件。
        这样即使写入过程中断电/崩溃，也不会损坏原始 data.json。
        """
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

        # 使用临时文件 + 原子 rename，确保不会写出半截 JSON
        dir_name = os.path.dirname(os.path.abspath(DataManager.FILE_NAME)) or "."
        # 创建临时文件与目标文件在同一目录（同一文件系统才能原子 rename）
        fd, temp_path = tempfile.mkstemp(
            suffix=".tmp",
            prefix="data_",
            dir=dir_name
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(
                    data,
                    f,
                    ensure_ascii=False,
                    indent=4
                )
            # 原子替换：Windows 上 os.replace 也是原子的
            target_path = os.path.join(dir_name, DataManager.FILE_NAME)
            os.replace(temp_path, target_path)
        except Exception:
            # 如果任何步骤失败，清理临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise

    @staticmethod
    def load_data():
        """从 JSON 文件加载数据到内存"""
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
