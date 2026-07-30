# 会员类
class Member:

    def __init__(self, id, name, phone, points, register_time):
        self.id = id
        self.name = name
        self.phone = phone
        self.points = points
        self.register_time = register_time

    # 对象转换成字典
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "points": self.points,
            "register_time": str(self.register_time)
        }

    # 字典转换成对象
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["name"],
            data["phone"],
            data["points"],
            data["register_time"]
        )


# 会员列表
class MemberList:
    member_list = []
