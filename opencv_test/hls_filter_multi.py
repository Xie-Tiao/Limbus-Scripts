import base64
import os
import time

import cv2
import flet as ft
import numpy as np

# 初始值
H_INIT = [0, 180]
L_INIT = [0, 255]
S_INIT = [0, 255]
THRESH = 36

image_list = [
    '1-4.png',
    '1-6.png',
]


def main(page: ft.Page):
    page.window_width = 1700
    page.window_height = 1000

    def update_images(_):
        for image_update in image_filter_list:
            image_update.update_image()
        time.sleep(0.1)
        page.update()

    h_slider = ft.RangeSlider(min=0, max=180, start_value=H_INIT[0], end_value=H_INIT[1], divisions=181,
                              label="{value} H",
                              on_change=update_images)
    l_slider = ft.RangeSlider(min=0, max=255, start_value=L_INIT[0], end_value=L_INIT[1], divisions=256,
                              label="{value} L",
                              on_change=update_images)
    s_slider = ft.RangeSlider(min=0, max=255, start_value=S_INIT[0], end_value=S_INIT[1], divisions=256,
                              label="{value} S",
                              on_change=update_images)
    factor_x_slider = ft.Slider(min=-3, max=3, value=0, label="{value} x", on_change=update_images)
    factor_y_slider = ft.Slider(min=-3, max=3, value=0, label="{value} y", on_change=update_images)
    factor_w_slider = ft.Slider(min=-3, max=3, value=1, label="{value} w", on_change=update_images)
    factor_h_slider = ft.Slider(min=-3, max=3, value=1, label="{value} h", on_change=update_images)
    kernel_size_slider = ft.Slider(min=1, max=31, value=1, divisions=31, label="kernel_size", on_change=update_images)
    hls_column = ft.Column(width=1700, height=900, scroll=ft.ScrollMode.AUTO)

    def str_to_int(value):
        return round(float(value))

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

    def rectangles_offset(rectangles, image, x_offset_factor=0, y_offset_factor=0, width_scale_factor=1,
                          height_scale_factor=1):
        # 获取图像的宽度和高度
        image_width = image.shape[1]
        image_height = image.shape[0]

        rectangles_list = [(max(0, round(x + w * x_offset_factor)),  # 确保x坐标不小于0
                            max(0, round(y + h * y_offset_factor)),  # 确保y坐标不小于0
                            min(image_width, round(w * width_scale_factor)),  # 确保宽度不超过图像宽度
                            min(image_height, round(h * height_scale_factor)))  # 确保高度不超过图像高度
                           for x, y, w, h in rectangles]

        return rectangles_list

    def convert_b64(image_cv2):
        encode_img = cv2.imencode('.jpg', image_cv2)
        b64_img = base64.b64encode(encode_img[1]).decode('utf-8')
        return b64_img

    class ImageFilter:
        def __init__(self, image_path):
            self.image_path = image_path
            self.original_image = cv2.imread(image_path)
            self.image_show = ft.Image(src_base64=convert_b64(self.original_image), width=800)
            self.image_output = ft.Image(src_base64=convert_b64(self.original_image), width=800)
            self.mask = np.zeros_like(self.original_image)
            hls_column.controls.append(ft.Row(controls=[self.image_show, self.image_output]))

        def apply_hsl_filter(self, image, h_range, s_range, l_range):
            h_channel, s_channel, l_channel = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HLS))
            h_mask = cv2.inRange(h_channel, h_range[0], h_range[1])
            s_mask = cv2.inRange(s_channel, s_range[0], s_range[1])
            l_mask = cv2.inRange(l_channel, l_range[0], l_range[1])
            self.mask = cv2.bitwise_and(h_mask, cv2.bitwise_and(s_mask, l_mask))

            # 对mask进行闭运算
            kernel_size = str_to_int(kernel_size_slider.value)
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            self.mask = cv2.morphologyEx(self.mask, cv2.MORPH_CLOSE, kernel)
            # 然后使用闭运算后的掩模来过滤图像
            filtered_image = cv2.bitwise_and(image, image, mask=self.mask)
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

            print(f'\'kernel_size\': {str_to_int(kernel_size_slider.value)},')

            return filtered_image

        def save_rectangles(self, image, rect, i):
            # 保存对应的图像区域到 /output 目录中
            x, y, w, h = rect
            roi = image[y:y + h, x:x + w]
            output_path = os.path.join('output', f'{self.image_path}rect_{i}.png')
            cv2.imwrite(output_path, roi)

        def draw_rectangles(self, image, rects, color=(255, 255, 0), thickness=2):
            # pass

            # image = image_binary
            i = 1000
            for rect in rects:
                self.save_rectangles(image, rect, i)
                i += 1
            for rect in rects:
                cv2.rectangle(image, rect[:2], (rect[0] + rect[2], rect[1] + rect[3]), color, thickness)
            self.image_output.src_base64 = convert_b64(image)

        def update_image(self):

            h_range = [str_to_int(h_slider.start_value), str_to_int(h_slider.end_value)]
            s_range = [str_to_int(s_slider.start_value), str_to_int(s_slider.end_value)]
            l_range = [str_to_int(l_slider.start_value), str_to_int(l_slider.end_value)]
            filtered_image = self.apply_hsl_filter(self.original_image, h_range, s_range, l_range)
            self.image_show.src_base64 = convert_b64(filtered_image)

            image = self.original_image.copy()
            # image_filtered = apply_hsl_filter(image, h_range=h_range, s_range=s_range, l_range=l_range)
            # _, image_binary = cv2.threshold(cv2.cvtColor(image_filtered, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_OTSU)

            # Detect rectangles and draw them on the image
            rectangles = find_bounding_boxes(self.mask, THRESH)
            rectangles_offset_list = rectangles_offset(
                rectangles,
                image,
                factor_x_slider.value,
                factor_y_slider.value,
                factor_w_slider.value,
                factor_h_slider.value,
            )
            # draw_rectangles_rotated(image, image_binary)
            self.draw_rectangles(image, rectangles_offset_list)

    # images_processor = ImageProcessor(page, ["path/to/image1.png", "path/to/image2.png"], [0, 180], [0, 255],
    #                                   [0, 255])

    image_filter_list = []
    for image_input in image_list:
        image_filter = ImageFilter(image_input)
        image_filter_list.append(image_filter)

    hls_column.controls.extend([
        h_slider,
        l_slider,
        s_slider,
        factor_x_slider,
        factor_y_slider,
        factor_w_slider,
        factor_h_slider,
        kernel_size_slider,
    ])

    page.add(hls_column)


ft.app(target=main)
