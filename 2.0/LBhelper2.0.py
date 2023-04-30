import pyautogui
import time
import xlrd
import pyperclip
import os

#定义鼠标事件
def mouseClick(clickTimes,lOrR,img,img_list,reTry,n):
    #执行一次
    if reTry == 1:
        for j in range(len(img_list)):
            location=pyautogui.locateCenterOnScreen(img,confidence=0.9)
            # print(location)
            if location is not None:
                pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
                print("正在左键",img)
                break
            else:
                print("未找到匹配图片,0.5秒后重试")
                time.sleep(0.5)
                break
        # 如果在for循环中没有找到匹配项，则输出错误消息。
        return False

    #-1代表一直重复
    elif reTry == -1: 
        while True:
            location=pyautogui.locateCenterOnScreen(img,confidence=0.9)
            if location is not None:
                pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
            time.sleep(0.1)
    
    #重复多次
    elif reTry > 1:
        i = 1
        while i < reTry + 1:
            location=pyautogui.locateCenterOnScreen(img,confidence=0.9)
            if location is not None:
                pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
                print("重复")
                i += 1
            time.sleep(0.1)

#定义图像判断事件
def checkpic(pic):
    #检查屏幕上是否出现了一个图像
    if pyautogui.locateOnScreen(pic,confidence=0.9) is not None:
        print('找到了',pic)
        return True

    else:
        print('没找到',pic)
        return False


#任务
def mainWork(img):
    i = 1
    while i < sheet1.nrows:
        #取本行指令的操作类型———————excel第一列
        cmdType = sheet1.row(i)[0]
        # print('cmdType=',cmdType)
        #1代表单击左键
        if cmdType.value == 1.0:
            #取图片名称——————excel第三列
            img_str = sheet1.row(i)[2].value
            img_list = img_str.split(",") # 使用逗号分割输入文本行
            img_list = [img.strip() for img in img_list] # 将元素中的空格清除
            n = len(img_list)
            # img = sheet1.row(i)[2].value
            # print('img='+img)
            reTry = 1
            # print(sheet1.row(i)[3].ctype)——————excecl第四列
            if sheet1.row(i)[3].ctype == 2 and sheet1.row(i)[3].value != 0:
                reTry = sheet1.row(i)[3].value
                print("reTry=",reTry)

            #取图片判断对象——————excel第二列
            pic = sheet1.row(i)[1].value
            # print(pic)
            piccheck = checkpic(pic)
            # print(piccheck)
            if piccheck:
                for img in img_list:
                    # img = img_list[n]
                    mouseClick(1,"left",img,img_list,reTry,n)
                    n = n-1
                    # print("单击左键",img)
                    # print(n)
            else:
                print('判断出错')
        #——————————————————————————————————————————————————————————————————                                       
        #5代表等待
        elif cmdType.value == 5.0:
            #取图片名称
            waitTime = sheet1.row(i)[2].value
            time.sleep(waitTime)
            print("等待",waitTime,"秒")
        #6代表滚轮
        elif cmdType.value == 6.0:
            #取图片名称
            scroll = sheet1.row(i)[2].value
            pyautogui.scroll(int(scroll))
            print("滚轮滑动",int(scroll),"距离")                      
        i += 1

# 数据检查
# cmdType.value  1.0 左键单击    2.0 左键双击  3.0 右键单击  4.0 输入  5.0 等待  6.0 滚轮
# ctype     空：0
#           字符串：1
#           数字：2
#           日期：3
#           布尔：4
#           error：5
def dataCheck(sheet1):
    checkCmd = True
    #行数检查
    if sheet1.nrows<2:
        print("没数据啊哥")
        checkCmd = False
    #每行数据检查
    i = 1
    while i < sheet1.nrows:
        # 第1列 操作类型检查
        cmdType = sheet1.row(i)[0]
        if cmdType.ctype != 2 or (cmdType.value != 1.0 and cmdType.value != 2.0 and cmdType.value != 3.0 
        and cmdType.value != 4.0 and cmdType.value != 5.0 and cmdType.value != 6.0):
            print('第',i+1,"行,第1列数据有毛病")
            checkCmd = False
        # 第2列 内容检查
        cmdValue = sheet1.row(i)[2]
        # 读图点击类型指令，内容必须为字符串类型
        if cmdType.value ==1.0 or cmdType.value == 2.0 or cmdType.value == 3.0:
            if cmdValue.ctype != 1:
                print('第',i+1,"行,第2列数据有毛病")
                checkCmd = False
        # 输入类型，内容不能为空
        if cmdType.value == 4.0:
            if cmdValue.ctype == 0:
                print('第',i+1,"行,第2列数据有毛病")
                checkCmd = False
        # 等待类型，内容必须为数字
        if cmdType.value == 5.0:
            if cmdValue.ctype != 2:
                print('第',i+1,"行,第2列数据有毛病")
                checkCmd = False
        # 滚轮事件，内容必须为数字
        if cmdType.value == 6.0:
            if cmdValue.ctype != 2:
                print('第',i+1,"行,第2列数据有毛病")
                checkCmd = False
        i += 1
    return checkCmd

if __name__ == '__main__':
    file = 'cmd.xls'
    #打开文件
    wb = xlrd.open_workbook(filename=file)
    #通过索引获取表格sheet页
    sheet1 = wb.sheet_by_index(0)
    print('【Limbus Helper Starting...10s后自动运行】——————————————————————————————————————————————————————')
    
    #数据检查
    checkCmd = dataCheck(sheet1)
    if checkCmd:
        while True:
            mainWork(sheet1)
            time.sleep(0.1)
            print("等待0.1秒")    
    else:
        print('输入有误或者已经退出!')
