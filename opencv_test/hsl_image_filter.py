import base64
import os
import time

import cv2
import flet as ft
import numpy as np

'''
gear: H:[15, 40]S:[30, 180]:L[40, 190]
skip: H12-25 S:150-210 L:20-200
encounters_flag: H:[10, 40]S:[50, 130]:L[30, 140]
yes_button: H:[12, 18]S:[100, 185]L:[30, 125]
high very high: H:[18, 30]S:[40, 170]L:[20, 255]


'back_button.png': [
            [9, 21],
            [10, 110],
            [40, 230]


'''
image_path = "1-2.png"  # Replace with the actual path to your image
thresh = 36


def convert_b64(image_cv2):
    encode_img = cv2.imencode('.jpg', image_cv2)
    b64_img = base64.b64encode(encode_img[1]).decode('utf-8')
    return b64_img


def main(page: ft.Page):
    page.window_width = 1700
    page.window_height = 900
    # image_path = "2-3.png"  # Replace with the actual path to your image
    original_image = cv2.imread(image_path)

    def update_image(_):
        def str_to_int(value):
            return round(float(value))

        h_range = [str_to_int(h_slider.start_value), str_to_int(h_slider.end_value)]
        s_range = [str_to_int(s_slider.start_value), str_to_int(s_slider.end_value)]
        l_range = [str_to_int(l_slider.start_value), str_to_int(l_slider.end_value)]
        filtered_image = apply_hsl_filter(original_image, h_range, s_range, l_range)
        image_show.src_base64 = convert_b64(filtered_image)
        image_show.update()

        image = original_image.copy()
        image_filtered = apply_hsl_filter(image, h_range=h_range, s_range=s_range, l_range=l_range)
        _, image_binary = cv2.threshold(cv2.cvtColor(image_filtered, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_OTSU)

        # Detect rectangles and draw them on the image
        rectangles = find_bounding_boxes(image_binary, thresh)
        rectangles_offset_list = rectangles_offset(
            rectangles,
            factor_x_slider.value,
            factor_y_slider.value,
            factor_w_slider.value,
            factor_h_slider.value,
        )
        # draw_rectangles_rotated(image, image_binary)
        draw_rectangles(image, rectangles_offset_list, image_binary)

    def find_bounding_boxes(image, threshold):
        contours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        bounding_rects = [cv2.boundingRect(c) for c in contours]
        sizes = [rect[2] * rect[3] for rect in bounding_rects]
        sizes = sorted(sizes, reverse=True)

        threshold_size = sizes[min(threshold - 1, len(sizes) - 1)]
        return [
            rect for rect in bounding_rects
            if rect[2] * rect[3] >= threshold_size and 0.1 <= rect[2] / rect[3] <= 10
            # 添加了新的条件，宽度和高度之间的比例应在 0.1 到 10 之间
        ]

    def rectangles_offset(rectangles, x_offset_factor=0, y_offset_factor=0, width_scale_factor=1,
                          height_scale_factor=1):
        image_width, image_height = 1920, 1080

        rectangles_list = [(max(0, round(x + w * x_offset_factor)),  # 确保x坐标不小于0
                            max(0, round(y + h * y_offset_factor)),  # 确保y坐标不小于0
                            min(image_width, round(w * width_scale_factor)),  # 确保宽度不超过图像宽度
                            min(image_height, round(h * height_scale_factor)))  # 确保高度不超过图像高度
                           for x, y, w, h in rectangles]

        return rectangles_list

    def apply_hsl_filter(image, h_range, s_range, l_range):
        h_channel, s_channel, l_channel = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HLS))
        h_mask = cv2.inRange(h_channel, h_range[0], h_range[1])
        s_mask = cv2.inRange(s_channel, s_range[0], s_range[1])
        l_mask = cv2.inRange(l_channel, l_range[0], l_range[1])
        mask = cv2.bitwise_and(h_mask, cv2.bitwise_and(s_mask, l_mask))
        filtered_image = cv2.bitwise_and(image, image, mask=mask)
        print(
            f'{tuple(h_range)},\n{tuple(s_range)},\n{tuple(l_range)}'
        )
        # print(f'H:{h_range}S:{s_range}L:{l_range}')
        # print(f'h_range={h_range}, s_range={s_range}, l_range={l_range}')
        try:
            print(
                f'({round(factor_x_slider.value, 2)}, {round(factor_y_slider.value, 2)}, {round(factor_w_slider.value, 2)}, {round(factor_h_slider.value, 2)})'
            )
        except NameError:
            pass

        return filtered_image

    def save_rectangles(image, rect, i):
        # 保存对应的图像区域到 /output 目录中
        x, y, w, h = rect
        roi = image[y:y + h, x:x + w]
        output_path = os.path.join('output', f'rect_{i}.png')
        cv2.imwrite(output_path, roi)

    def draw_rectangles(image, rects, image_binary, color=(255, 255, 0), thickness=2):
        # pass
        time.sleep(0.1)
        # image = image_binary
        i = 1000
        for rect in rects:
            save_rectangles(image, rect, i)
            i += 1
        for rect in rects:
            cv2.rectangle(image, rect[:2], (rect[0] + rect[2], rect[1] + rect[3]), color, thickness)
        image_output.src_base64 = convert_b64(image)
        image_output.update()

    def draw_rectangles_rotated(image, image_binary):
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

        image_output.src_base64 = convert_b64(image)
        image_output.update()

    # H:[0, 30]S:[0, 90]L:[0, 180]
    h_range = [0, 180]
    s_range = [0, 255]
    l_range = [0, 255]
    image_show = ft.Image(src_base64=convert_b64(original_image), width=800)
    image_output = ft.Image(src_base64=convert_b64(original_image), width=800)

    filtered_image = apply_hsl_filter(original_image, h_range, s_range, l_range)
    image_show.src_base64 = convert_b64(filtered_image)
    h_slider = ft.RangeSlider(min=0, max=180, start_value=h_range[0], end_value=h_range[1], divisions=181,
                              label="{value} H",
                              on_change=update_image)
    s_slider = ft.RangeSlider(min=0, max=255, start_value=s_range[0], end_value=s_range[1], divisions=256,
                              label="{value} S",
                              on_change=update_image)
    l_slider = ft.RangeSlider(min=0, max=255, start_value=l_range[0], end_value=l_range[1], divisions=256,
                              label="{value} L",
                              on_change=update_image)
    factor_x_slider = ft.Slider(min=-3, max=3, value=0, label="{value} x", on_change=update_image)
    factor_y_slider = ft.Slider(min=-3, max=3, value=0, label="{value} y", on_change=update_image)
    factor_w_slider = ft.Slider(min=-3, max=3, value=1, label="{value} w", on_change=update_image)
    factor_h_slider = ft.Slider(min=-3, max=3, value=1, label="{value} h", on_change=update_image)

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(controls=[image_show, image_output]),
                h_slider,
                s_slider,
                l_slider,
                factor_x_slider,
                factor_y_slider,
                factor_w_slider,
                factor_h_slider,
            ],
        )
    )


ft.app(target=main)
