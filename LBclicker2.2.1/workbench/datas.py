# import flet as ft
from flet import ImageFit,Image
from pandas import DataFrame
# import pandas as pd

# 创建一个空的 4x3 数据框架
cmd = DataFrame(index=range(4), columns=range(3))
waittime = 0.3

# 为每个单元格赋值
cmd.loc[0, 0] = '1'
cmd.loc[0, 1] = '1.png'
cmd.loc[0, 2] = '1.png'
cmd.loc[1, 0] = '5'
cmd.loc[1, 1] = ''
cmd.loc[1, 2] = waittime
cmd.loc[2, 0] = '1'
cmd.loc[2, 1] = '2.png'
cmd.loc[2, 2] = '3_1.png,3_2.png,3_3.png,3_4.png'
cmd.loc[3, 0] = '5'
cmd.loc[3, 1] = ''
cmd.loc[3, 2] = waittime

img_Laetitia = Image(src="./assets/Wich.webp", height= 260,fit=ImageFit.FIT_HEIGHT,tooltip="程序已在运行...")
img_Monster = Image(src="./assets/LaetitiaMinionCrop.webp", width= 800,fit=ImageFit.FIT_WIDTH)