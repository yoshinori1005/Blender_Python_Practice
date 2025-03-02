import bpy


# 基本的なクラス
class PrintColor:
    def __init__(self, color="red"):
        self.color = color

    def print_color(self):
        print(f"The color is {self.color}")


my_color = PrintColor()
my_color.print_color()
my_color2 = PrintColor(color="green")
my_color2.print_color()


# クラス変数の利用
class InstanceCount:
    instance_count = 0

    def __init__(self):
        InstanceCount.instance_count += 1

    # クラス変数のようにクラスから直接使用できる書き方
    @classmethod
    def get_instance_count(cls):
        print(f"Instance count:{cls.instance_count}")


# @classmethodを使った際の呼び出し方
a = InstanceCount()
InstanceCount.get_instance_count()
b = InstanceCount()
InstanceCount.get_instance_count()
