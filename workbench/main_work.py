import json
import os
import time

import cv2
import numpy as np
import pyautogui as pg
from PIL import ImageGrab

from workbench import SettingsReader
from workbench import mouse_control
from workbench.image_processing import ImageDetector
from workbench.ocr_utils import Ocr
from . import file_path_utils

pg.FAILSAFE = False

_worklist_path = os.path.join(file_path_utils.PathManager.CURRENT_DIR, 'worklist.json')
with open(_worklist_path, 'r', encoding='utf-8') as f:
    _worklist = json.load(f)


def get_screenshot():
    # 获取屏幕截图
    image = ImageGrab.grab()

    # 转换为opencv的数据格式
    # noinspection PyTypeChecker
    opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return opencv_image


# 界面检查模块
def check_img(img, confid=0.9):
    try:
        if pg.locateOnScreen(file_path_utils.PathManager.get_local_image(img), confidence=confid) is not None:
            print('看到了...', img)
            return True
    except pg.ImageNotFoundException:
        print('没看到..', img)
        return False


def check_img_list(img_list, confid=0.9):
    for i in range(len(img_list)):
        if check_img(img_list[i], confid):
            return True
    return False


# 控制模块
def mouse_click(img, times=1, confid=0.9):
    try:
        location = pg.locateCenterOnScreen(file_path_utils.PathManager.get_local_image(img), confidence=confid)
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
            print("点到了 ...", img)
    except pg.ImageNotFoundException:
        print("没点到 ...", img)


def mouse_click_img_list(img_list, times=1, confid=0.9):
    for i in range(len(img_list)):
        if mouse_click(img_list[i], times, confid):
            return True
    return False


def mouse_hold(img, confid=0.75):
    try:
        location = pg.locateCenterOnScreen(file_path_utils.PathManager.get_local_image(img), confidence=confid)
        if location is not None:
            pg.click(
                x=location.x + (-27),
                y=location.y + 117,
                interval=0,
                duration=0,
                clicks=1,
                button='left',
            )
            print('点到了模糊的...', img)
            pg.mouseDown(
                x=location.x + (-27),
                y=location.y + 117,
                duration=0,
                button='left',
            )
            print('按住模糊的..', img)
    except pg.ImageNotFoundException:
        print("没按住 ...", img)


def mouse_hold_img_list(img_list, confid=0.75):
    for i in range(len(img_list)):
        if mouse_hold(img_list[i], confid):
            return True
    return False


def abnormality_ocr():
    # text_rect_list = screenshot_ocr()
    image = get_screenshot()
    dict_key = 'choices'
    image_detector = ImageDetector(image, dict_key, 12)
    rectangles_list = image_detector.find_bounding_boxes()

    text_rect_list = Ocr.recognize_rectangles(image, rectangles_list)
    match, rect, score = Ocr.get_best_choice(text_rect_list)
    print(f'match,{match} rect,{rect} score{score}')
    if score > 60:
        mouse_control.click_rect_center(rect)
    else:
        mouse_click_img_list(_worklist['abnormality_click'])


# ————————————————————————————————————————————————————
# ————————————————————————————————————————————————————
# 按界面归类组件
def battle_field():
    battle_checked = check_img_list(_worklist['battle_checked'])
    if battle_checked:
        mouse_click("gear_1690.png")
        mouse_click("gear_fullscreen.png")
        pg.press('p')
        time.sleep(0.5)  # 让游戏\\gear反应一下
        lang = SettingsReader.read_option('Language', 'current')
        bad_checked = check_img_list(_worklist[f'bad_checked_{lang}'], confid=0.75)
        print('123')
        death_checked = check_img_list(_worklist[f'death_checked_{lang}'])
        if death_checked:
            mouse_click_img_list(_worklist['death_click'])
            # 暂时将就用这个，以后改
            time.sleep(5)
            stage_field()
        elif SettingsReader.read_option('EGO', 'value') == 'True':
            if bad_checked:
                mouse_hold_img_list(_worklist[f'bad_checked_{lang}'], confid=0.75)
                time.sleep(2)  # 让游戏\\ego反应一下
                if check_img_list(_worklist['ego_click']):
                    mouse_click_img_list(_worklist['ego_click'], 4)
                    pg.press('p')
                    pg.press('p')
                else:
                    mouse_click_img_list(_worklist['property'], 2)
        pg.press('enter')
    else:
        pass


def encounters_field():
    encounters_checked = check_img_list(_worklist['encounters_checked'])
    store_checked = check_img_list(_worklist['store_checked'])
    chair_checked = check_img_list(_worklist['chair_checked'])
    if encounters_checked:
        mouse_click_img_list(_worklist['encounters_click'][0], 3)
        mouse_click_img_list(_worklist['encounters_click'][1])
        if store_checked:
            time.sleep(0.5)
            mouse_click_img_list(_worklist['store_click'])
            print('store空着的...')
        elif chair_checked:
            time.sleep(0.5)
            mouse_click_img_list(_worklist['chair_click'])
            print('chair空着的...')
        else:
            abnormality_ocr()
            lang = SettingsReader.read_option('Language', 'current')
            vote_checked = check_img_list(_worklist[f'vote_checked_{lang}'])
            if vote_checked:
                mouse_click_img_list(_worklist[f'vote_click_{lang}'], confid=0.95)
            else:
                pass
    else:
        print('654')
        pass


def stage_field():
    stage_checked = check_img_list(_worklist['stage_checked'])
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
