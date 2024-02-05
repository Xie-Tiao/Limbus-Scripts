import pyautogui

# from pyautogui import locateCenterOnScreen, click, locateOnScreen
# import time
import datas

pyautogui.FAILSAFE = False


# 定义鼠标事件
def mouseClick(clickTimes, lOrR, img, img_list, n):
    for j in range(len(img_list)):
        try:
            location = pyautogui.locateCenterOnScreen("./assets/" + img, confidence=0.9)
            if location is not None:
                pyautogui.click(
                    location.x,
                    location.y,
                    clicks=clickTimes,
                    interval=0.2,
                    duration=0.2,
                    button=lOrR,
                )
                print("Clicking ", img)
                break
        except pyautogui.ImageNotFoundException:
            print("Try Again ...")
            # time.sleep(0.0)
            break
    # 如果在for循环中没有找到匹配项，则输出错误消息。
    return False


# 定义图像判断事件
def checkpic(pic):
    # 检查屏幕上是否出现了一个图像
    try:
        if pyautogui.locateOnScreen("./assets/" + pic, confidence=0.9) is not None:
            print("Checked", pic)
            return True

    except Exception as e:
        print("Failed to check", pic)
        return False


def MainWork():
    i = 0
    while i < len(datas.cmd):
        cmdType = float(datas.cmd.loc[i][0])
        # 1代表单击左键
        if cmdType == 1.0:
            # 取图片名称——————第三列
            img_str = datas.cmd.loc[i][2]
            img_list = img_str.split(",")  # 使用逗号分割输入文本行
            img_list = [img.strip() for img in img_list]  # 将元素中的空格清除
            n = len(img_list)

            # 取图片判断对象——————第二列
            pic = datas.cmd.loc[i][1]
            piccheck = checkpic(pic)
            if piccheck:
                for img in img_list:
                    mouseClick(1, "left", img, img_list, n)
                    n = n - 1
            else:
                print("Something went wrong in Checking Part")

        # 2代表左键多次点击，比如4次
        if cmdType == 2.0:
            # 取图片名称——————第三列
            img_str = datas.cmd.loc[i][2]
            img_list = img_str.split(",")  # 使用逗号分割输入文本行
            img_list = [img.strip() for img in img_list]  # 将元素中的空格清除
            n = len(img_list)

            # 取图片判断对象——————第二列
            pic = datas.cmd.loc[i][1]
            piccheck = checkpic(pic)
            if piccheck:
                for img in img_list:
                    mouseClick(3, "left", img, img_list, n)
                    n = n - 1
            else:
                print("Something went wrong in Checking Part")

        # 5代表等待
        elif cmdType == 5.0:
            # 取图片名称
            waitTime = datas.cmd.loc[i][2]
            # time.sleep(waitTime)
            print("Waiting", waitTime, "")

        i += 1

# if __name__ == '__main__':
#     while True:
#         MainWork()
