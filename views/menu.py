from views.product_view import ProductView
from views.member_view import MemberView
from views.cashier_view import CashierView
from views.order_view import OrderView


class Menu:

    def start(self):

        while True:

            print(
                """
                ========================
                   便利店零售管理系统
                ========================
                
                1. 商品管理
                
                2. 会员管理
                
                3. 收银结算
                
                4. 订单查询
                
                0. 退出系统
                
                ========================
                """
            )

            choice = input("请选择功能:")
            if choice == "1":
                ProductView.menu()
            elif choice == "2":
                MemberView.menu()
            elif choice == "3":
                CashierView.start()
            elif choice == "4":
                OrderView.menu()
            elif choice == "0":
                print("系统退出")
                break
            else:
                print("输入错误，请重新选择")
