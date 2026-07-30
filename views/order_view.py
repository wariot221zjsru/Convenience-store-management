from services.order_query_service import OrderQueryService


class OrderView:

    @staticmethod
    def menu():

        while True:

            print(
                """
                ========订单查询========
                
                1. 查看全部订单
                
                2. 查询订单详情
                
                3. 查询会员订单
                
                0. 返回
                
                =======================
                """
            )

            choice = input("请选择:")
            if choice == "1":
                OrderQueryService.check_order()
            elif choice == "2":
                OrderQueryService.select_by_order_id()
            elif choice == "3":
                OrderQueryService.select_by_member_phone()
            elif choice == "0":
                break
            else:
                print("输入错误")
