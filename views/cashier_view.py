from services.order_service import OrderService


class CashierView:

    @staticmethod
    def start():
        cart = []

        print("开始收银")
        OrderService.add_cart(cart)

        if not cart:
            print("购物车为空")
            return

        OrderService.show_cart(cart)

        confirm = input("是否结算?(y/n):")

        if confirm.lower() == "y":
            OrderService.checkout(cart)

        else:
            print("取消结算")
