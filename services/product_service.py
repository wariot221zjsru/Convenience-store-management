from models.product import *
from services.transaction import Transaction, TransactionError


class ProductService:

    # 录入商品（事务保护）
    @staticmethod
    def add_product():
        while True:
            pid = input("请输入商品ID:")
            exist = False

            for p in ProductList.product_list:
                if p.id == pid:
                    exist = True
                    print("该商品ID已存在！")
                    break

            if exist:
                continue

            while True:
                name = input("请输入商品名称:")

                if not name:
                    print("名称不能为空！")
                    continue

                break

            while True:
                try:
                    price = float(input("请输入商品单价:"))

                    if price <= 0:
                        print("单价必须大于0")
                        continue

                    break

                except ValueError:
                    print("请输入数字！")

            while True:
                try:
                    stock = int(input("请输入商品库存:"))

                    if stock < 0:
                        print("库存不能为负数")
                        continue

                    break

                except ValueError:
                    print("请输入整数！")

            category = input("请输入商品分类:")

            product = Product(pid, name, price, stock, category)

            # ---- 事务保护 ----
            try:
                with Transaction("商品录入"):
                    ProductList.product_list.append(product)
                print("商品添加成功！")
            except TransactionError as e:
                print(f"商品添加失败: {e}")
            break

    # 展示所有商品
    @staticmethod
    def check_product():
        if not ProductList.product_list:
            print("暂无商品")
            return

        print(
            f"{'商品ID':<15}"
            f"{'名称':<15}"
            f"{'单价':<15}"
            f"{'库存':<15}"
            f"{'分类':<15}"
        )

        for product in ProductList.product_list:
            print(
                f"{product.id:<15}"
                f"{product.name:<15}"
                f"{product.price:<15}"
                f"{product.stock:<15}"
                f"{product.category:<15}"
            )

    # 修改商品信息（事务保护）
    @staticmethod
    def update_product():
        pid = input("请输入修改商品ID:")

        for product in ProductList.product_list:
            if product.id == pid:
                name = input("新的商品名称:")

                if name:
                    product.name = name

                price = input("新的商品价格:")

                if price:
                    try:
                        price = float(price)

                        if price <= 0:
                            print("价格必须大于0")
                            return

                        product.price = price

                    except ValueError:
                        print("价格格式错误")
                        return

                stock = input("新的库存:")

                if stock:
                    try:
                        stock = int(stock)

                        if stock < 0:
                            print("库存不能为负")
                            return

                        product.stock = stock

                    except ValueError:
                        print("库存格式错误")
                        return

                category = input("新的分类(回车跳过):")

                if category:
                    product.category = category

                # ---- 事务保护 ----
                try:
                    with Transaction("商品修改"):
                        pass  # 修改已在内存中完成，事务负责持久化
                    print("修改成功！")
                except TransactionError as e:
                    print(f"修改失败: {e}")
                return

        print("商品不存在！")

    # 删除商品（事务保护）
    @staticmethod
    def delete_product():
        pid = input("请输入删除商品ID:")

        for product in ProductList.product_list:
            if product.id == pid:
                confirm = input("确认删除？(y/n):")

                if confirm.lower() == "y":
                    # ---- 事务保护 ----
                    try:
                        with Transaction("商品删除"):
                            ProductList.product_list.remove(product)
                        print("删除成功")
                    except TransactionError as e:
                        print(f"删除失败: {e}")

                return

        print("商品不存在")

    # 入库操作（事务保护）
    @staticmethod
    def stock_input():
        pid = input("请输入商品ID:")

        for product in ProductList.product_list:
            if product.id == pid:
                num = int(input("入库数量:"))

                if num <= 0:
                    print("入库必须为正数")
                    return

                # ---- 事务保护 ----
                try:
                    with Transaction("商品入库"):
                        product.stock += num
                    print("入库成功")
                except TransactionError as e:
                    print(f"入库失败: {e}")
                    # 库存已通过事务回滚恢复
                return

        print("商品不存在")

    # 出库操作（事务保护）
    @staticmethod
    def stock_output():
        pid = input("请输入商品ID:")

        for product in ProductList.product_list:
            if product.id == pid:
                num = int(input("出库数量:"))

                if num <= 0:
                    print("请输入正数")
                    return

                if num > product.stock:
                    print("库存不足，禁止超卖")
                    return

                # ---- 事务保护 ----
                try:
                    with Transaction("商品出库"):
                        product.stock -= num
                    print("出库成功")
                except TransactionError as e:
                    print(f"出库失败: {e}")
                    # 库存已通过事务回滚恢复
                return

        print("商品不存在")
