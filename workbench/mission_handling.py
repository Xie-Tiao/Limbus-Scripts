import configparser
import time

import cv2
import numpy as np
from PIL import ImageGrab

from workbench import file_path_utils
from workbench import mouse_control

config = configparser.ConfigParser()

# from workbench import keyboard_control
hsl = 'hsl'
mask_param = 'mask_param'
offset_param = 'offset_param'
template_dict = {
    'skip_button.png': {
        'hsl': (
            (12, 25),
            (150, 210),
            (20, 200)
        )
    },
    'back_button.png': {
        'hsl': (
            (9, 21),
            (10, 110),
            (40, 230)
        ),
        'mask_param': (
            2 / 3,
            3 / 4,
        )

    },
    'yes_button_Japanese.png': {
        'hsl': (
            (12, 18),
            (100, 185),
            (30, 125)
        )
    },
    'very_high_Japanese.png': {
        'hsl': (
            (18, 30),
            (40, 170),
            (20, 255)
        ),
        'offset_param': (0, -0.61, 1, 0.55),
    },
    'high_Japanese.png': {
        'hsl': (
            (0, 30),
            (0, 255),
            (0, 255)
        )
    },
}


def get_screenshot():
    # 获取屏幕截图
    image = ImageGrab.grab()

    # 转换为opencv的数据格式
    # noinspection PyTypeChecker
    opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return opencv_image


def apply_hsl_filter(image, h_range, s_range, l_range):
    hls_channels = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HLS))
    mask = cv2.bitwise_and(
        cv2.inRange(hls_channels[0], *h_range),
        cv2.inRange(hls_channels[1], *s_range),
        cv2.inRange(hls_channels[2], *l_range)
    )
    return cv2.bitwise_and(image, image, mask=mask)


def find_bounding_boxes(image, threshold):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bounding_rects = [cv2.boundingRect(c) for c in contours]
    sizes = [rect[2] * rect[3] for rect in bounding_rects]
    sizes = sorted(sizes, reverse=True)

    threshold_size = sizes[min(threshold - 1, len(sizes) - 1)]
    return [
        rect for rect in bounding_rects
        if rect[2] * rect[3] >= threshold_size and 0.1 <= rect[2] / rect[3] <= 10
    ]


def calculate_similarity(image, template: cv2.typing.MatLike):
    # 调整图片大小
    # target_size = (template.shape[1], template.shape[0])
    # image = cv2.resize(image, target_size)
    mask = cv2.inRange(image, np.array([0, 0, 0]), np.array([255, 255, 255]))
    # 创建ORB特征提取器
    orb = cv2.ORB.create(edgeThreshold=0)

    # 从两幅图像中查找关键点和描述符
    kp1, des1 = orb.detectAndCompute(image, mask)
    kp2, des2 = orb.detectAndCompute(template, mask)

    # 创建Brute Force Matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)  # 修改为False，以便返回两个最近的匹配点

    # 使用Matcher匹配描述符
    matches = bf.knnMatch(des1, des2, k=2)  # 修改为knnMatch，以便返回两个最近的匹配点

    # 应用比例测试，过滤掉明显不匹配的点
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:  # 如果第一个匹配点的距离小于第二个匹配点的距离的0.75倍，那么它是好的匹配点
            good_matches.append(m)

    # 根据好的匹配数返回相似度
    return len(good_matches)


def check_and_click(image, target, current_language=None, thresh=30):
    if current_language is None:
        confidence, rect = get_confidence_rect(image, f'{target}.png')
    else:
        confidence, rect = get_confidence_rect(image, f'{target}_{current_language}.png')
    print(f'confidence: {confidence}')
    if confidence > thresh:
        mouse_control.click_rect_center(rect)


def test():
    image = get_screenshot()
    image_name = 'very_high_Japanese.png'

    confidence, rect = get_confidence_rect(image, image_name)
    print(f'confidence: {confidence}')


def main():
    config.read(file_path_utils.settings_path)
    current_language = config['Language']['current']
    image = get_screenshot()
    # 先判断状态
    battle_confidence = 0
    # battle_confidence, battle_rect = get_confidence_rect(image, 'gear.png')
    encounters_confidence, skip_rect = get_confidence_rect(image, 'skip_button.png')

    # logging_utils.logger.info(f'battle_confidence: {battle_confidence}')
    # print(f'battle_confidence: {battle_confidence}')
    # print(f'encounters_confidence: {encounters_confidence}')

    if battle_confidence > 20 and encounters_confidence < 10:
        # keyboard_control.keyboard.press_keys()
        pass
    elif battle_confidence < 10 and encounters_confidence > 20:
        # 找back_button
        back_button_confidence, back_button_rect = get_confidence_rect(image, 'back_button.png')
        print(f'back_button_confidence: {back_button_confidence}')
        if back_button_confidence > 30:
            mouse_control.click_rect_center(back_button_rect)
            time.sleep(1)
            check_and_click(image, 'yes_button', current_language)
        check_and_click(image, 'very_high', current_language)
        # click skip button
        # mouse_control.click_skip_button(skip_rect)

    # cv2.imshow("1", image)
    # cv2.waitKey(0)

# if __name__ == '__main__':
#     main()
