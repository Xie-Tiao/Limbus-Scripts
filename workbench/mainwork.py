import pyautogui

import workbench.datas as datas

pyautogui.FAILSAFE = False


# 定义鼠标事件
def mouse_click(click_times, left_or_right, img, img_list,n):
    for j in range(len(img_list)):
        try:
            location = pyautogui.locateCenterOnScreen("./assets/" + img, confidence=0.9)
            if location is not None:
                pyautogui.click(
                    location.x,
                    location.y,
                    clicks=click_times,
                    interval=0.2,
                    duration=0.2,
                    button=left_or_right,
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
def check_pic(pic):
    # 检查屏幕上是否出现了一个图像
    try:
        if pyautogui.locateOnScreen("./assets/" + pic, confidence=0.9) is not None:
            print("Checked", pic)
            return True

    except pyautogui.ImageNotFoundException:
        print("Failed to check", pic)
        return False


def main_work():
    i = 0
    while i < len(datas.cmd):
        cmd_type = float(datas.cmd.loc[i][0])
        # 1代表单击左键
        if cmd_type == 1.0:
            # 取图片名称——————第三列
            img_str = datas.cmd.loc[i][2]
            img_list = img_str.split(",")  # 使用逗号分割输入文本行
            img_list = [img.strip() for img in img_list]  # 将元素中的空格清除
            n = len(img_list)

            # 取图片判断对象——————第二列
            pic = datas.cmd.loc[i][1]
            is_pic_valid = check_pic(pic)
            if is_pic_valid:
                for img in img_list:
                    mouse_click(1, "left", img, img_list, n)
                    n = n - 1
            else:
                print("Something went wrong in Checking Part")

        # 2代表左键多次点击，比如4次
        if cmd_type == 2.0:
            # 取图片名称——————第三列
            img_str = datas.cmd.loc[i][2]
            img_list = img_str.split(",")  # 使用逗号分割输入文本行
            img_list = [img.strip() for img in img_list]  # 将元素中的空格清除
            n = len(img_list)

            # 取图片判断对象——————第二列
            pic = datas.cmd.loc[i][1]
            is_pic_valid = check_pic(pic)
            if is_pic_valid:
                for img in img_list:
                    mouse_click(3, "left", img, img_list, n)
                    n = n - 1
            else:
                print("Something went wrong in Checking Part")

        # 5代表等待
        elif cmd_type == 5.0:
            # 取图片名称
            wait_time = datas.cmd.loc[i][2]
            # time.sleep(wait_time)
            print("Waiting", wait_time, "")

        i += 1

# if __name__ == '__main__':
#     while True:
#         MainWork()
