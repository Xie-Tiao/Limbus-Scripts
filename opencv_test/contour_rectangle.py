import os

import cv2


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
        if rect[2] * rect[3] >= threshold_size and 0.1 <= rect[2] / rect[3] <= 10  # 添加了新的条件，宽度和高度之间的比例应在 0.1 到 10 之间
    ]


def draw_rectangles(image, rects, color=(0, 255, 0), thickness=2):
    i = 1000
    for rect in rects:
        save_rectangles(image, rect, i)
        i += 1
    for rect in rects:
        cv2.rectangle(image, rect[:2], (rect[0] + rect[2], rect[1] + rect[3]), color, thickness)


def save_rectangles(image, rect, i):
    # 保存对应的图像区域到 /output 目录中
    x, y, w, h = rect
    roi = image[y:y + h, x:x + w]
    output_path = os.path.join('output', f'rect_{i}.png')
    cv2.imwrite(output_path, roi)


def main():
    # Load and pre-process the image
    # image = cv2.imread("2-3.png")
    # image_filtered = apply_hsl_filter(image, h_range=[12, 25], s_range=[150, 210], l_range=[20, 200])
    image = cv2.imread("origin/3500.png")
    image_filtered = apply_hsl_filter(image, h_range=[0, 30], s_range=[0, 90], l_range=[0, 180])
    _, image_binary = cv2.threshold(cv2.cvtColor(image_filtered, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_OTSU)

    # Detect rectangles and draw them on the image
    rectangles = find_bounding_boxes(image_binary, 20)
    draw_rectangles(image, rectangles)

    cv2.imshow("Image with rectangles", image)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
