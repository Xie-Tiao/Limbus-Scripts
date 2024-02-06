import os

import cv2
import numpy as np
from PIL import ImageGrab

# from workbench import keyboard_control

# 获取assets的相对路径
current_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_path)
assets_relpath = os.path.join(current_dir, '../assets')


def get_local_image(image_name):
    return os.path.join(assets_relpath, image_name)


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
    target_size = (template.shape[1], template.shape[0])
    image = cv2.resize(image, target_size)
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


def get_confidence_rect(image, template_name):
    hsl_dict = {
        'gear.png': [
            [15, 40],
            [30, 180],
            [40, 190]
        ],
        'skip_button.png': [
            [12, 25],
            [150, 210],
            [20, 200]
        ]
    }
    # Load and pre-process the image
    image_filtered = apply_hsl_filter(
        image,
        h_range=hsl_dict[template_name][0],
        s_range=hsl_dict[template_name][1],
        l_range=hsl_dict[template_name][2]
    )
    _, image_binary = cv2.threshold(cv2.cvtColor(image_filtered, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_BINARY)

    # Detect rectangles and draw them on the image
    rectangles = find_bounding_boxes(image_binary, 12)

    # Load the skip button template
    template = cv2.imread(get_local_image(template_name))
    # template = cv2.imread(get_local_image('skip_button.png'))

    # Initialize maximum similarity and corresponding rectangle
    max_similarity = 0
    max_similarity_rect = None

    # Calculate similarity for each rectangle
    for rect in rectangles:
        x, y, w, h = rect
        roi = image[y:y + h, x:x + w]
        similarity = calculate_similarity(roi, template)

        # Update max similarity and max similarity rectangle if necessary
        if similarity > max_similarity:
            max_similarity = similarity
            max_similarity_rect = rect

        # cv2.imshow("12", roi)
        # print(f"Similarity for rectangle at ({x}, {y}) is {similarity:.4f}")
        # cv2.waitKey(0)

    # Return max similarity and it's corresponding rectangle
    return max_similarity, max_similarity_rect


def main():
    image = get_screenshot()
    # 先判断状态
    battle_confidence, battle_rect = get_confidence_rect(image, 'gear.png')
    encounters_confidence, mission2_rect = get_confidence_rect(image, 'skip_button.png')
    print(f'battle_confidence: {battle_confidence}')
    print(f'encounters_confidence_confidence: {encounters_confidence}')
    if battle_confidence > 10 * encounters_confidence:
        # keyboard_control.keyboard.press_keys()
        pass
    elif battle_confidence * 10 < encounters_confidence:
        pass

    # cv2.imshow("1", image)
    # cv2.waitKey(0)


if __name__ == '__main__':
    main()
