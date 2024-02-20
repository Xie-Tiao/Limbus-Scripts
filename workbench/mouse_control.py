import time
from workbench.read_settings import SettingsReader
from ctypes import windll, Structure, c_ulong, byref


class PointAPI(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]


def get_mouse_position():
    po = PointAPI()
    windll.user32.GetCursorPos(byref(po))
    return int(po.x), int(po.y)


def move_mouse(x, y):
    current_DPI = SettingsReader.read_option('DPI', 'current')
    x = round(x / (current_DPI * 0.01))
    y = round(y / (current_DPI * 0.01))
    windll.user32.SetCursorPos(x, y)


def click_mouse():
    # 模拟鼠标左键按下和释放
    windll.user32.mouse_event(2, 0, 0, 0, 0)  # 鼠标左键按下
    windll.user32.mouse_event(4, 0, 0, 0, 0)  # 鼠标左键释放


def click_mouse_after_moveto(x, y):
    move_mouse(x, y)
    click_mouse()


def click_rect_center(rect):
    time.sleep(0.2)
    x, y = get_center(rect)
    click_mouse_after_moveto(x, y)
    time.sleep(0.2)
    move_mouse(0, 0)
    # 


def click_skip_button(rect):
    x, y = get_center(rect)
    move_mouse(x, y)

    for _ in range(4):
        click_mouse()
        time.sleep(0.2)
    move_mouse(0, 0)
    # time.sleep(1)


def get_center(rect):
    x, y, w, h = rect
    center_x = round(x + w / 2)
    center_y = round(y + h / 2)
    return center_x, center_y


def click_intensity(text_rect_list, target_texts):
    # if current_language == 'jp':
    #     target_texts = ['常に高', '高い', '普通', '低い', '常に低']
    # elif current_language == 'kr':
    #     target_texts = ['常に高', '高い', '普通', '低い', '常に低']
    # else:
    #     target_texts = ['常に高', '高い', '普通', '低い', '常に低']

    for target_text in target_texts:
        for text, rect in text_rect_list:
            if target_text in text:
                click_rect_center(rect)
                return


if __name__ == "__main__":
    click_rect_center((1044, 399, 693, 98))
    # # 获取当前鼠标位置
    current_x, current_y = get_mouse_position()
    print(f"当前鼠标位置：({current_x}, {current_y})")
   
    # # 移动鼠标到指定位置
    # target_x, target_y = 900, 300
    # move_mouse(target_x, target_y)
    # print(f"移动鼠标到：({target_x}, {target_y})")

    # # 模拟点击鼠标
    # click_mouse()
    # print("模拟点击鼠标左键")
