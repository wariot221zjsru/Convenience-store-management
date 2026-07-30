from dao.data_manager import DataManager
from views.menu import Menu

if __name__ == "__main__":

    # 启动加载数据
    DataManager.load_data()
    menu = Menu()
    menu.start()
