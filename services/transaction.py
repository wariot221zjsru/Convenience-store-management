from copy import deepcopy
from models.product import ProductList
from models.member import MemberList
from models.order import OrderList
from dao.data_manager import DataManager


class TransactionError(Exception):
    """事务异常，用于标识事务层面的错误"""

    def __init__(self, message):
        super().__init__(message)


class Transaction:
    """
    事务管理器 —— 提供真正的一次性事务与异常回滚能力。

    特性：
    - 上下文管理器协议 (with Transaction(...) as txn: ...)
    - begin():  深拷贝三张核心表（商品/会员/订单）作为快照
    - commit(): 持久化到磁盘，成功后清除快照
    - rollback(): 用快照恢复内存中的三张表
    - 发生任何异常时 __exit__ 自动回滚，保证数据不外泄
    - 正常退出时自动提交
    """

    def __init__(self, name: str = "未命名事务"):
        self.name = name
        self._product_backup = None
        self._member_backup = None
        self._order_backup = None
        self._active = False

    # ------------------------------------------------------------------
    # 核心 API
    # ------------------------------------------------------------------

    def begin(self):
        """开启事务，对当前内存数据做全量深拷贝快照"""
        if self._active:
            raise TransactionError(f"事务 '{self.name}' 已经处于活动状态，请勿重复 begin()")
        self._product_backup = deepcopy(ProductList.product_list)
        self._member_backup = deepcopy(MemberList.member_list)
        self._order_backup = deepcopy(OrderList.order_list)
        self._active = True
        print(f"[事务] '{self.name}' 开始 -- 快照已建立")

    def commit(self):
        """
        提交事务：
        1. 将当前内存数据写入磁盘（原子写入）
        2. 清除快照
        若写盘失败，自动触发 rollback()
        """
        if not self._active:
            raise TransactionError(f"事务 '{self.name}' 未开始，无法提交")
        try:
            DataManager.save_data()
            self._clear_backup()
            self._active = False
            print(f"[事务] '{self.name}' 提交成功 [OK]")
        except Exception as e:
            self.rollback()
            raise TransactionError(f"事务 '{self.name}' 提交失败: {e}") from e

    def rollback(self):
        """
        回滚事务：
        用之前保存的快照覆盖内存中的三张核心表，完全恢复到事务开始前的状态。
        """
        if not self._active:
            return
        if self._product_backup is not None:
            ProductList.product_list = self._product_backup
        if self._member_backup is not None:
            MemberList.member_list = self._member_backup
        if self._order_backup is not None:
            OrderList.order_list = self._order_backup
        self._clear_backup()
        self._active = False
        print(f"[事务] '{self.name}' 已回滚 -- 数据已恢复到事务开始前的状态 [ROLLBACK]")

    def is_active(self) -> bool:
        """查询事务是否处于活动状态"""
        return self._active

    # ------------------------------------------------------------------
    # 上下文管理器 (with 语句)
    # ------------------------------------------------------------------

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # 业务代码中抛出了异常 → 自动回滚
            self.rollback()
            print(f"[事务] '{self.name}' 因异常自动回滚 ({exc_type.__name__}: {exc_val})")
            return False  # 不吞掉异常，让调用方感知
        else:
            # 正常走完 → 提交
            try:
                self.commit()
            except TransactionError:
                # commit 内部已经 rollback 了，这里把异常继续抛出
                raise
        return False

    # ------------------------------------------------------------------
    # 内部工具
    # ------------------------------------------------------------------

    def _clear_backup(self):
        """清空快照引用，释放内存"""
        self._product_backup = None
        self._member_backup = None
        self._order_backup = None
