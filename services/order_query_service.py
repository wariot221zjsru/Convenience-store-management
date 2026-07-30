from models.order import *
from models.member import *


class OrderQueryService:

    # 列表展示全部订单
    @staticmethod
    def check_order():
        if not OrderList.order_list:
            print("暂无订单")
            return

        print(
            f"{'订单号':<20}"
            f"{'会员身份':<15}"
            f"{'实付金额':<15}"
            f"{'支付方式':<15}"
            f"{'交易时间':<20}"
        )

        for order in OrderList.order_list:
            member = (
                order.member_id
                if order.member_id
                else "散客"
            )

            print(
                f"{order.order_id:<20}"
                f"{member:<15}"
                f"{order.real_amount:<15}"
                f"{order.pay_method:<15}"
                f"{str(order.trading_hour):<20}"
            )

    # 根据订单号查询
    @staticmethod
    def select_by_order_id():

        oid = input("请输入订单号:")

        for order in OrderList.order_list:
            if order.order_id == oid:
                OrderQueryService.show_order_detail(order)
                return

        print("订单不存在！")

    # 根据会员手机号查询
    @staticmethod
    def select_by_member_phone():

        phone = input("请输入会员手机号:")
        exist = False

        for order in OrderList.order_list:
            if order.member_phone == phone:
                exist = True
                OrderQueryService.show_order_detail(order)

        if not exist:
            print("该会员没有订单记录！")

    # 展示订单详情
    @staticmethod
    def show_order_detail(order):
        print("""==========订单详情==========""")
        print(f"订单号:{order.order_id}")
        print(f"会员ID:{order.member_id if order.member_id else '散客'}")
        print(f"交易时间:{order.trading_hour}")
        print("--------商品明细--------")
        print(
            f"{'商品':<15}"
            f"{'单价':<10}"
            f"{'数量':<10}"
            f"{'小计':<10}"
        )

        for item in order.items:
            print(
                f"{item.product_name:<15}"
                f"{item.price:<10}"
                f"{item.quantity:<10}"
                f"{item.subtotal:<10}"
            )

        print("-----------------------")
        print(f"原价金额:{order.total_amount}")
        print(f"实付金额:{order.real_amount}")
        print(f"支付方式:{order.pay_method}")
        print(f"获得积分:{order.points}")
        print("========================")
