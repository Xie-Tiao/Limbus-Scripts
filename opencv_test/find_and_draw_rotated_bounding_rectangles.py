import cv2
import numpy as np


def extract_and_save_rotated_rect(img, rect):
    h, w = img.shape[:2]  # 原图像的长和宽
    box = np.intp(cv2.boxPoints(rect))
    rect_w, rect_h = round(rect[1][0]), round(rect[1][1])  # 最小外接矩形的宽和高
    margin = 0
    if rect_w <= rect_h:
        x, y = int(box[1][0]), int(box[1][1])  # 旋转中心
        M2 = cv2.getRotationMatrix2D((x, y), rect[2], 1)
        rotated_image = cv2.warpAffine(img, M2, (w * 2, h * 2))
        y1, y2 = y - margin if y - margin > 0 else 0, y + rect_h + margin + 1
        x1, x2 = x - margin if x - margin > 0 else 0, x + rect_w + margin + 1
        rotated_rect_img = rotated_image[y1: y2, x1: x2]

        # 保存包含旋转矩形区域的新图像
        cv2.imwrite('output_rotated_rect.png', rotated_rect_img)
        cv2.imshow('output_rotated_rect.png', rotated_rect_img)
        cv2.waitKey(0)
    else:
        x, y = int(box[2][0]), int(box[2][1])  # 旋转中心
        M2 = cv2.getRotationMatrix2D((x, y), rect[2] + 90, 1)
        rotated_image = cv2.warpAffine(img, M2, (w * 2, h * 2))
        y1, y2 = y - margin if y - margin > 0 else 0, y + rect_w + margin + 1
        x1, x2 = x - margin if x - margin > 0 else 0, x + rect_h + margin + 1
        rotated_rect_img = rotated_image[y1: y2, x1: x2]

    return rotated_rect_img


def find_min_area_rectangles(image_path):
    # 读取图像
    image = cv2.imread(image_path)

    h_range = (0, 3)
    l_range = (0, 255)
    s_range = (0, 255)
    h_channel, s_channel, l_channel = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HLS))
    h_mask = cv2.inRange(h_channel, h_range[0], h_range[1])
    l_mask = cv2.inRange(l_channel, l_range[0], l_range[1])
    s_mask = cv2.inRange(s_channel, s_range[0], s_range[1])
    mask = cv2.bitwise_and(h_mask, cv2.bitwise_and(s_mask, l_mask))
    filtered_image = cv2.bitwise_and(image, image, mask=mask)

    # 执行阈值处理或其他预处理以获取二值图像
    _, image_binary = cv2.threshold(cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_OTSU)

    # 寻找轮廓
    contours, _ = cv2.findContours(image_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 绘制所有轮廓的最小外接矩形
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)

        # 绘制旋转矩形

        if 63 < rect[-1] < 66:
            print(rect)
            # extract_and_save_rotated_rect(image, rect)
            cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

    # 显示或保存带有矩形的图像
    cv2.imshow("Rotated Bounding Rectangles", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 使用示例：
# find_min_area_rectangles('output/rect_1000.png')
find_min_area_rectangles("origin/3450.png")
