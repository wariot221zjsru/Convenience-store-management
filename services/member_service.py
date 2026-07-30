from models.member import *
from dao.data_manager import DataManager
from datetime import datetime


class MemberService:

    # 录入会员
    @staticmethod
    def member_register():
        while True:

            mid = input("请输入会员ID:")
            exist = False

            for member in MemberList.member_list:
                if member.id == mid:
                    exist = True
                    print("会员ID已存在！")
                    break

            if exist:
                continue

            name = input("请输入姓名:")

            while not name:
                print("姓名不能为空！")
                name = input("请输入姓名:")

            while True:
                phone = input("请输入手机号:")

                if not phone:
                    print("手机号不能为空！")
                    continue

                if not phone.isdigit():
                    print("手机号必须是数字！")
                    continue

                if len(phone) != 11:
                    print("手机号必须11位！")
                    continue

                phone_exist = False
                for member in MemberList.member_list:
                    if member.phone == phone:
                        phone_exist = True
                        break

                if phone_exist:
                    print("手机号已经注册！")
                    continue
                break

            points = 0
            register_time = datetime.now().date()
            member = Member(mid, name, phone, points, register_time)
            MemberList.member_list.append(member)
            DataManager.save_data()

            print("会员注册成功！")
            break

    # 列表展示所有会员
    @staticmethod
    def check_member():

        if not MemberList.member_list:
            print("暂无会员")
            return

        print(
            f"{'会员ID':<15}"
            f"{'姓名':<15}"
            f"{'手机号':<15}"
            f"{'积分':<15}"
            f"{'注册时间':<15}"
        )

        for member in MemberList.member_list:
            print(
                f"{member.id:<15}"
                f"{member.name:<15}"
                f"{member.phone:<15}"
                f"{member.points:<15}"
                f"{member.register_time:<15}"
            )

    # 手机号查询会员
    @staticmethod
    def select_member():

        phone = input("请输入会员手机号:")

        for member in MemberList.member_list:
            if member.phone == phone:
                print(
                    f"""
                    会员ID:{member.id}
                    姓名:{member.name}
                    手机号:{member.phone}
                    积分:{member.points}
                    注册时间:{member.register_time}
                    """
                )
                return

        print("会员不存在！")

    # 积分转换
    @staticmethod
    def points_conversion(amount):
        return int(amount)

    # 会员95折
    @staticmethod
    def vip_amount(amount):
        return round(amount * 0.95,2)

    # 增加积分
    @staticmethod
    def add_points(member, amount):
        points = MemberService.points_conversion(amount)
        member.points += points
        DataManager.save_data()
