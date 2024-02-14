import ctypes
import time


# 定义一个键盘类，用于模拟键盘按键的操作
class KeyBoard:
    # 定义按键的虚拟键码映射
    key_values = {
        'shift': 0x10,
        'ctrl': 0x11,
        'alt': 0x12,
        'enter': 0x0D
    }

    for i in range(26):
        key_values[chr(65 + i).lower()] = 0x41 + i

    # 定义按键的操作,表示按键的升起和落下
    KEY_EVENT_KEYDOWN = 0x0
    KEY_EVENT_KEYUP = 0x2

    # 引用用户32库，用以发送按键消息
    user32 = ctypes.windll.user32

    # 定义一个私有函数，用于按下一个键
    # 参数key是要按下的键的名字，比如'a'或'shift'
    def __press_one_key(self, key):
        self.user32.keybd_event(self.key_values[key], 0, self.KEY_EVENT_KEYDOWN, 0)

    # 定义一个私有函数，用于释放一个键
    # 参数key是要释放的键的名字，比如'a'或'shift'
    def __release_one_key(self, key):
        self.user32.keybd_event(self.key_values[key], 0, self.KEY_EVENT_KEYUP, 0)

    # 定义一个公开函数，用于按下多个键
    # 参数keys是要按下的键的名字的字符串，用' + '分隔，比如'shift + ctrl + alt + D'
    def press_keys(self, keys: str):
        keys = keys.lower().split(' + ')
        for key in keys:
            self.__press_one_key(key)
        # 短暂等待，确保按键消息已送达
        time.sleep(0.01)
        # 释放按键
        for key in keys:
            self.__release_one_key(key)


# 创建一个键盘对象
keyboard = KeyBoard()

if __name__ == '__main__':
    # 测试函数
    # keyboard.press_keys("shift + ctrl + alt + D")
    # keyboard.press_keys("alt + C")
    keyboard.press_keys("D")
