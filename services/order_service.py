from models.member import *
from models.product import *
from models.order import *
from services.member_service import MemberService
from dao.data_manager import DataManager
from datetime import datetime


class OrderService:

    # 会员身份识别
    @staticmethod
    def identification():

        phone = input("请输入会员手机号(回车跳过):")

        if phone == "":
            return None

        for member in MemberList.member_list:
            if member.phone == phone:
                print("会员识别成功！")
                return member

        print("未找到会员，按散客结算")
        return None

    # 添加购物车
    @staticmethod
    def add_cart(cart):
        while True:

            pid = input("请输入商品ID(ID为0结束):")

            if pid == "0":
                break

            for product in ProductList.product_list:
                if product.id == pid:
                    while True:

                        try:
                            count = int(input("请输入购买数量:"))

                            if count <= 0:
                                print("数量必须大于0")
                                continue

                            if count > product.stock:
                                print("库存不足")
                                continue

                            break

                        except ValueError:
                            print("请输入整数")

                    item = OrderItem(product.id, product.name, product.price, count)
                    cart.append(item)
                    print(f"{product.name} 已加入购物车")
                    break

            else:
                print("商品不存在")

            choice = input("是否还要继续购买商品:(y/n)")
            if choice.upper() == "N":
                break

    # 展示购物车
    @staticmethod
    def show_cart(cart):
        total = 0
        print("==========购物车==========")
        print(
            f"{'商品':<15}"
            f"{'单价':<10}"
            f"{'数量':<10}"
            f"{'小计':<10}"
        )

        for item in cart:
            print(
                f"{item.product_name:<15}"
                f"{item.price:<10}"
                f"{item.quantity:<10}"
                f"{item.subtotal:<10}"
            )
            total += item.subtotal
        print(f"原价总金额:{total}")
        return total

    # 结算
    @staticmethod
    def checkout(cart):

        if not cart:
            print("购物车为空")
            return

        # 辨别是否是会员
        member = OrderService.identification()
        total_amount = 0
        for item in cart:
            total_amount += item.subtotal
        real_amount = total_amount
        points = 0

        # 会员优惠
        if member:
            real_amount = MemberService.vip_amount(total_amount)
            points = MemberService.points_conversion(real_amount)
        print(f"应付金额:{real_amount}")
        pay_method = input("支付方式(现金/微信/支付宝):")

        for item in cart:
            for product in ProductList.product_list:
                if product.id == item.product_id:
                    product.stock -= item.quantity

        # 创建订单
        order_id = str(datetime.now().strftime("%Y%m%d%H%M%S"))
        order = Order(order_id, cart, member.phone if member else None, member.id if member else None, total_amount, real_amount, points, pay_method, datetime.now())
        OrderList.order_list.append(order)

        # 增加积分
        if member:
            member.points += points
        DataManager.save_data()
        print("结算成功！")
        OrderService.print_ticket(order)

    # 打印发票
    @staticmethod
    def print_ticket(order):

        print("""==========便利店小票==========""")
        print("订单号:", order.order_id)
        print("交易时间:", order.trading_hour)
        for item in order.items:
            print(item.product_name, item.quantity, item.subtotal)

        print("实付金额:", order.real_amount)
        print("支付方式:", order.pay_method)
        print("获得积分:", order.points)
        print("==========================")
