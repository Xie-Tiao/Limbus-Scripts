import time

import cv2
import numpy as np
from PIL import ImageGrab

from workbench import mouse_control
from workbench.image_processing import ImageDetector
from workbench.ocr_utils import Ocr
from workbench.read_settings import SettingsReader


# from workbench import keyboard_control


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
    match, rect, score = Ocr.get_best_match(text_rect_list)
    print(f'match,{match} rect,{rect} score{score}')
    if score > 80:
        mouse_control.click_rect_center(rect)


def test():
    image = get_screenshot()
    image_name = 'very_high_Japanese.png'
    image_detector = ImageDetector(image, image_name)

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


def test_choices():
    image = get_screenshot()
    dict_key = 'choices'
    image_detector = ImageDetector(image, dict_key, 12)
    rectangles_list = image_detector.find_bounding_boxes()

    text_rect_list = Ocr.recognize_rectangles(image, rectangles_list)
    match, rect, score = Ocr.get_best_match(text_rect_list)
    print(f'match,{match} rect,{rect} score{score}')
    # mouse_control.click_rect_center(rect)


def main():
    image = get_screenshot()
    current_language = SettingsReader.read_option('Language', 'current')
    # 先判断状态
    battle_confidence = 0
    # battle_confidence, battle_rect = get_confidence_rect(image, 'gear.png')
    skip_button_detector = ImageDetector(image, 'skip_button.png')
    encounters_confidence, skip_rect = skip_button_detector.get_confidence_rect()

    # logging_utils.logger.info(f'battle_confidence: {battle_confidence}')
    # print(f'battle_confidence: {battle_confidence}')
    # print(f'encounters_confidence: {encounters_confidence}')

    if battle_confidence > 20 and encounters_confidence < 10:
        # keyboard_control.keyboard.press_keys()
        pass
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


if __name__ == '__main__':
    main()
