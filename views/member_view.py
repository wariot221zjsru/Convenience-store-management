from services.member_service import MemberService


class MemberView:

    @staticmethod
    def menu():

        while True:

            print(
                """
                ========会员管理========
                
                1. 注册会员
                
                2. 查看会员
                
                3. 查询会员
                
                0. 返回
                
                =======================
                """
            )

            choice = input("请选择:")
            if choice == "1":
                MemberService.member_register()
            elif choice == "2":
                MemberService.check_member()
            elif choice == "3":
                MemberService.select_member()
            elif choice == "0":
                break
            else:
                print("输入错误")
