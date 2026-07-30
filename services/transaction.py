from copy import deepcopy
from models.product import ProductList
from models.member import MemberList
from models.order import OrderList


# 事务模块
class Transaction:

    def __init__(self):
        self.product_backup = None
        self.member_backup = None
        self.order_backup = None

    # 开启事务
    def begin(self):
        # 深拷贝保存当前状态
        self.product_backup = deepcopy(
            ProductList.product_list
        )
        self.member_backup = deepcopy(
            MemberList.member_list
        )
        self.order_backup = deepcopy(
            OrderList.order_list
        )
        print("事务开始")

    # 提交事务
    def commit(self):
        self.product_backup = None
        self.member_backup = None
        self.order_backup = None
        print("事务提交成功")

    # 回滚事务
    def rollback(self):
        ProductList.product_list = (self.product_backup)
        MemberList.member_list = (self.member_backup)
        OrderList.order_list = (self.order_backup)
        print("事务失败，数据已恢复")
