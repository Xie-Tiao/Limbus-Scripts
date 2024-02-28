import pyautogui as pg
import json
import os
import time

import cv2
import numpy as np
from PIL import ImageGrab
from workbench.ocr_utils import Ocr
from workbench import mouse_control
from workbench.image_processing import ImageDetector

from . import file_path_utils

# import file_path_utils

pg.FAILSAFE = False

_worklist_path = os.path.join(file_path_utils.PathManager.CURRENT_DIR, 'worklist.json')
with open(_worklist_path, 'r', encoding='utf-8') as f:
    _worklist = json.load(f)

low_confidence = 0.75


def get_screenshot():
    # 获取屏幕截图
    image = ImageGrab.grab()

    # 转换为opencv的数据格式
    # noinspection PyTypeChecker
    opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return opencv_image


# 界面检查模块
def check_img(img):
    try:
        if pg.locateOnScreen(file_path_utils.PathManager.get_local_image(img), confidence=0.9) is not None:
            print('看到了...', img)
            return True
    except pg.ImageNotFoundException:
        return False


def check_img_list(img_list):
    for i in range(len(img_list)):
        if check_img(img_list[i]):
            return True
    return False


def check_low_img(img):
    try:
        if pg.locateOnScreen(file_path_utils.PathManager.get_local_image(img), confidence=low_confidence) is not None:
            print('看到了模糊的...', img)
            return True
    except pg.ImageNotFoundException:
        return False


def check_low_img_list(img_list):
    for i in range(len(img_list)):
        if check_low_img(img_list[i]):
            return True
    return False


# 控制模块
def mouse_click(img, times=1):
    try:
        location = pg.locateCenterOnScreen(file_path_utils.PathManager.get_local_image(img), confidence=0.9)
        if location is not None:
            pg.click(
                location.x,
                location.y,
                interval=0.1,
                duration=0,
                clicks=times,
                button='left',
            )
            pg.moveTo(0, 0)
    except pg.ImageNotFoundException:
        print("没点到 ...", img)


def mouse_click_img_list(img_list, times=1):
    for i in range(len(img_list)):
        if mouse_click(img_list[i], times):
            return True
    return False


def mouse_hold(img):
    try:
        location = pg.locateCenterOnScreen(file_path_utils.PathManager.get_local_image(img), confidence=low_confidence)
        if location is not None:
            pg.click(
                x=location.x + (-27),
                y=location.y + 117,
                interval=0,
                duration=0,
                clicks=2,
                button='left',
            )
            print('双击了模糊的...', img)
            pg.mouseDown(
                x=location.x + (-27),
                y=location.y + 117,
                duration=0,
                button='left',
            )
            print('按住模糊的..', img)
    except pg.ImageNotFoundException:
        print("没按住 ...", img)


def mouse_hold_img_list(img_list):
    for i in range(len(img_list)):
        if mouse_hold(img_list[i]):
            return True
    return False


# ————————————————————————————————————————————————————
# 按界面归类组件
def battle_field():
    battle_checked = check_img_list(_worklist['battle_checked'])
    if battle_checked:
        mouse_click("gear_1690.png")
        mouse_click("gear_fullscreen.png")
        pg.press('p')
        time.sleep(0.5)  # 让游戏\\gear反应一下
        bad_checked = check_low_img_list(_worklist['bad_checked'])
        death_checked = check_img_list(_worklist['death_checked'])
        if death_checked:
            mouse_click_img_list(_worklist['death_click'])
        else:
            pass
        if bad_checked:
            mouse_hold_img_list(_worklist['bad_checked'])
            time.sleep(2)  # 让游戏\\ego反应一下
            mouse_click_img_list(_worklist['ego_click'], 4)
            pg.press('p')
            pg.press('p')
        else:
            pass
        pg.press('enter')

    else:
        pass


def encounters_field():
    encounters_checked = check_img_list(_worklist['encounters_checked'])
    store_checked = check_img_list(_worklist['store_checked'])
    if encounters_checked:
        mouse_click_img_list(_worklist['encounters_click'][0], 3)
        mouse_click_img_list(_worklist['encounters_click'][1])
        if store_checked:
            time.sleep(0.5)
            mouse_click_img_list(_worklist['store_click'])
            print('store空着的...')
        else:
            abnormality_ocr()
            vote_checked = check_img_list(_worklist['vote_checked'])
            if vote_checked:
                mouse_click_img_list(_worklist['vote_click'])
            else:
                pass
    else:
        print('654')
        pass


def abnormality_ocr():
    # text_rect_list = screenshot_ocr()
    image = get_screenshot()
    dict_key = 'choices'
    image_detector = ImageDetector(image, dict_key, 12)
    rectangles_list = image_detector.find_bounding_boxes()

    text_rect_list = Ocr.recognize_rectangles(image, rectangles_list)
    match, rect, score = Ocr.get_best_choice(text_rect_list)
    print(f'match,{match} rect,{rect} score{score}')
    if score > 74:
        mouse_control.click_rect_center(rect)
    else:
        mouse_click_img_list(_worklist['abnormality_click'])


def stage_field():
    stage_checked = check_img_list(_worklist['stage_checked'])
    print('123')
    if stage_checked:
        mouse_click_img_list(_worklist['stage_click'])
        pg.press('enter')
        time.sleep(2)
        pg.press('enter')
    else:
        pass


def main():
    battle_field()
    encounters_field()


if __name__ == '__main__':
    while True:
        battle_field()

        # stage_field()
        encounters_field()
