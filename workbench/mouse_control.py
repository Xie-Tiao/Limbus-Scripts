from ctypes import windll, Structure, c_ulong, byref


class PointAPI(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]


def get_mouse_position():
    po = PointAPI()
    windll.user32.GetCursorPos(byref(po))
    return int(po.x), int(po.y)


def move_mouse(x, y):
    windll.user32.SetCursorPos(x, y)


def click_mouse():
    # 模拟鼠标左键按下和释放
    windll.user32.mouse_event(2, 0, 0, 0, 0)  # 鼠标左键按下
    windll.user32.mouse_event(4, 0, 0, 0, 0)  # 鼠标左键释放


def click_mouse_after_moveto(x, y):
    move_mouse(x, y)
    click_mouse()


if __name__ == "__main__":
    # 获取当前鼠标位置
    current_x, current_y = get_mouse_position()
    print(f"当前鼠标位置：({current_x}, {current_y})")

    # 移动鼠标到指定位置
    target_x, target_y = 900, 300
    move_mouse(target_x, target_y)
    print(f"移动鼠标到：({target_x}, {target_y})")

    # 模拟点击鼠标
    click_mouse()
    print("模拟点击鼠标左键")
