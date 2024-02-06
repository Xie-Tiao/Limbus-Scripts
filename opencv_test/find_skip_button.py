import cv2
import numpy as np


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


def main():
    # Load and pre-process the image
    image = cv2.imread("3-1.png")
    size_list = [960, 540]

    image = cv2.resize(image, [int(x * 0.8) for x in size_list])
    image_filtered = apply_hsl_filter(image, h_range=[12, 25], s_range=[150, 210], l_range=[20, 200])
    _, image_binary = cv2.threshold(cv2.cvtColor(image_filtered, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_BINARY)

    # Detect rectangles and draw them on the image
    rectangles = find_bounding_boxes(image_binary, 12)

    # Load the skip button template
    skip_button_template = cv2.imread("skip_button_2.png")

    # Calculate similarity for each rectangle
    for rect in rectangles:
        x, y, w, h = rect
        roi = image[y:y + h, x:x + w]
        similarity = calculate_similarity(roi, skip_button_template)
        cv2.imshow("12", roi)
        print(f"Similarity for rectangle at ({x}, {y}) is {similarity:.4f}")
        cv2.waitKey(0)


if __name__ == "__main__":
    main()
