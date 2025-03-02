import bpy

# 基本的なクラス
class PrintColor:
    def __init__(self,color=None):
        if color is None:
            self.color="red"
        else:
            self.color=color
    
    def print_color(self):
        print(f"The color is {self.color}")

my_color=PrintColor()
my_color.print_color()
my_color2=PrintColor(color="green")
my_color.print_color()