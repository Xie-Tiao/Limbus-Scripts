# # import flet as ft
# from flet import ImageFit, Image
# from pandas import DataFrame
#
# # import pandas as pd
#
# # 创建一个空的 8x3 数据框架
# cmd = DataFrame(index=range(8), columns=range(3))
# wait_time = 0.0
#
# # 为每个单元格赋值
# cmd.loc[0, 0] = '1'
# cmd.loc[0, 1] = '1.png'
# cmd.loc[0, 2] = '1.png'
# cmd.loc[1, 0] = '5'
# cmd.loc[1, 1] = ''
# cmd.loc[1, 2] = wait_time
# cmd.loc[2, 0] = '1'
# cmd.loc[2, 1] = '2.png'
# cmd.loc[2, 2] = '3_2.png,3_3.png,3_4.png'
# cmd.loc[3, 0] = '5'
# cmd.loc[3, 1] = ''
# cmd.loc[3, 2] = wait_time
# cmd.loc[4, 0] = '2'
# cmd.loc[4, 1] = '4.png'
# cmd.loc[4, 2] = '4_1.png,4_1_2.png'
# cmd.loc[5, 0] = '5'
# cmd.loc[5, 1] = ''
# cmd.loc[5, 2] = wait_time
# cmd.loc[6, 0] = '1'
# cmd.loc[6, 1] = '4.png'
# cmd.loc[6, 2] = '4_11.png,4_6.png,4_12.png,4_4.png,4_10.png,4_2.png,4_5.png,4_7_2.png,4_7_1.png,4_7.png,4_8.png,4_9.png'
# cmd.loc[7, 0] = '5'
# cmd.loc[7, 1] = ''
# cmd.loc[7, 2] = wait_time
#
# img_Laetitia = Image(src="./assets/Wich.webp", height=260, fit=ImageFit.FIT_HEIGHT, tooltip="程序已在运行...")
# img_Monster = Image(src="./assets/LaetitiaMinionCrop.webp", width=800, fit=ImageFit.FIT_WIDTH)
