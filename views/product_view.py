from services.product_service import ProductService


class ProductView:

    @staticmethod
    def menu():
        while True:

            print(
                """
                ========商品管理========
                
                1. 添加商品
                
                2. 查看商品
                
                3. 修改商品
                
                4. 删除商品
                
                5. 商品入库
                
                6. 商品出库
                
                0. 返回
                
                =======================
                """
            )

            choice = input("请选择:")
            if choice == "1":
                ProductService.add_product()
            elif choice == "2":
                ProductService.check_product()
            elif choice == "3":
                ProductService.update_product()
            elif choice == "4":
                ProductService.delete_product()
            elif choice == "5":
                ProductService.stock_input()
            elif choice == "6":
                ProductService.stock_output()
            elif choice == "0":
                break
            else:
                print("输入错误")
