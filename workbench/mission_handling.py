import time

import cv2
import numpy as np
from PIL import ImageGrab

from workbench import keyboard_control
from workbench import mouse_control
from workbench.image_processing import ImageDetector
from workbench.ocr_utils import Ocr
from workbench.read_settings import SettingsReader

english_ocr_engine = Ocr('English')


def get_screenshot():
    # 获取屏幕截图
    image = ImageGrab.grab()

    # 转换为opencv的数据格式
    # noinspection PyTypeChecker
    opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return opencv_image


def check_and_click_image(image, target: str, current_language: str | None = None, thresh=30):
    if current_language is None:
        template_name = f'{target}.png'
    else:
        template_name = f'{target}_{current_language}.png'

    image_detector = ImageDetector(image, template_name)
    confidence, rect = image_detector.get_confidence_rect()
    print(f'confidence: {confidence}')
    if confidence > thresh:
        mouse_control.click_rect_center(rect)
        return True
    else:
        return False


def check_and_click_intensity(image):
    dict_key = 'intensity'
    image_detector = ImageDetector(image, dict_key, 20)
    rectangles_list = image_detector.find_bounding_boxes()
    text_rect_list = Ocr.recognize_rectangles(image, rectangles_list)
    mouse_control.click_intensity(text_rect_list, ['常に高', '高い', '通', '低い', '常に低'])


def check_and_click_choices(image):
    dict_key = 'choices'
    image_detector = ImageDetector(image, dict_key, 12)
    rectangles_list = image_detector.find_bounding_boxes()

    text_rect_list = Ocr.recognize_rectangles(image, rectangles_list)
    match, rect, score = Ocr.get_best_choice(text_rect_list)
    print(f'match,{match} rect,{rect} score{score}')
    if score > 80:
        mouse_control.click_rect_center(rect)


def check_and_click_text(image, dict_key, text, rect_thresh=12, score_thresh=75):
    image_detector = ImageDetector(image, dict_key, rect_thresh)
    rectangles_list = image_detector.find_bounding_boxes()

    match, rect, score = Ocr.check_text_in_rectangles_cls(image, rectangles_list, text)
    print(f'match,{match} rect,{rect} score{score}')
    if score > score_thresh:
        mouse_control.click_rect_center(rect)
        return True
    else:
        return False


def test():
    image = get_screenshot()
    image_name = 'setting_button.png'
    image_detector = ImageDetector(image, image_name, 36)
    confidence, rect = image_detector.get_confidence_rect()
    print(f'confidence: {confidence}')


def test_ocr():
    image = get_screenshot()
    dict_key = 'intensity'
    image_detector = ImageDetector(image, dict_key, 20)
    rectangles_list = image_detector.find_bounding_boxes()
    print(len(rectangles_list))
    text_rect_list = Ocr.recognize_rectangles(image, rectangles_list)
    mouse_control.click_intensity(text_rect_list, ['常に高', '高い', '通', '低い', '常に低'])


def test_ocr_2():
    image = get_screenshot()
    image_detector = ImageDetector(image, 'setting_button.png', 36)
    rectangles_list = image_detector.find_bounding_boxes()
    _, _, score = english_ocr_engine.check_text_in_rectangles(image, rectangles_list, 'MAX')
    print(score)


def test_ocr_3():
    image = get_screenshot()
    image_detector = ImageDetector(image, 'setting_menu', 36)
    rectangles_list = image_detector.find_bounding_boxes()
    _, _, score = Ocr.check_text_in_rectangles_cls(image, rectangles_list, 'MAX')
    print(score)


def test_choices():
    image = get_screenshot()
    dict_key = 'choices'
    image_detector = ImageDetector(image, dict_key, 12)
    rectangles_list = image_detector.find_bounding_boxes()

    text_rect_list = Ocr.recognize_rectangles(image, rectangles_list)
    match, rect, score = Ocr.get_best_choice(text_rect_list)
    print(f'match,{match} rect,{rect} score{score}')
    # mouse_control.click_rect_center(rect)

def main():
    image = get_screenshot()
    current_language = SettingsReader.read_option('Language', 'current')
    # 先判断状态
    setting_button_detector = ImageDetector(image, 'setting_button.png', 36)
    setting_button_rectangles_list = setting_button_detector.find_bounding_boxes()
    _, _, battle_confidence = english_ocr_engine.check_text_in_rectangles(image, setting_button_rectangles_list, 'MAX')
    
    skip_button_detector = ImageDetector(image, 'skip_button.png')
    encounters_confidence, skip_rect = skip_button_detector.get_confidence_rect()

    # logging_utils.logger.info(f'battle_confidence: {battle_confidence}')
    print(f'battle_confidence: {battle_confidence}')
    print(f'encounters_confidence: {encounters_confidence}')

    if battle_confidence > 40 and encounters_confidence < 10:
        time.sleep(0.2)
        keyboard_control.keyboard.press_keys('P')
        death_detector = ImageDetector(image, 'death_Japanese.png', 36)
        death_confidence, _ = death_detector.get_confidence_rect()
        gear_detector = ImageDetector(image, 'gear.png', 12)
        gear_confidence, _ = gear_detector.get_confidence_rect()
        gear_active_detector = ImageDetector(image, 'gear_active.png', 12)
        gear_active_confidence, _ = gear_active_detector.get_confidence_rect()
        print(gear_confidence,'---',gear_active_confidence)
        if death_confidence > 18:
            _, setting_rect = setting_button_detector.get_confidence_rect()
            mouse_control.click_rect_center(setting_rect)
            time.sleep(0.6)
            click_flag = check_and_click_text(image, 'setting_menu', 'Cステージリトライ')
            if click_flag is False:
                check_and_click_text(image, 'setting_menu', 'メステージをギブアップ')
        elif gear_confidence > 160:
            keyboard_control.keyboard.press_keys('P')
        elif gear_active_confidence > 0:
            keyboard_control.keyboard.press_keys('enter')

    elif battle_confidence < 10 and encounters_confidence > 20:
        # 找back_button
        back_button_detector = ImageDetector(image, 'back_button.png')
        back_button_confidence, back_button_rect = back_button_detector.get_confidence_rect()
        print(f'back_button_confidence: {back_button_confidence}')
        if back_button_confidence > 30:
            mouse_control.click_rect_center(back_button_rect)
            time.sleep(1)
            check_and_click_image(image, 'yes_button', current_language)
            check_and_click_intensity(image)
        # 找选项
        check_and_click_choices(image)
        # click skip button
        mouse_control.click_skip_button(skip_rect)

    

# if __name__ == '__main__':
#     image = get_screenshot()
#     image_detector = ImageDetector(image, 'gear.png', 12)
#     gear_confidence, _ = image_detector.get_confidence_rect()
#     print(gear_confidence)
