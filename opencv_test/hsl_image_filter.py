import base64

import cv2
import flet as ft

'''
gear: H:[15, 40]S:[30, 180]:L[40, 190]
skip: H12-25 S:150-210 L:20-200



'''


def apply_hsl_filter(image, h_range, s_range, l_range):
    h_channel, s_channel, l_channel = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HLS))
    h_mask = cv2.inRange(h_channel, h_range[0], h_range[1])
    s_mask = cv2.inRange(s_channel, s_range[0], s_range[1])
    l_mask = cv2.inRange(l_channel, l_range[0], l_range[1])
    mask = cv2.bitwise_and(h_mask, cv2.bitwise_and(s_mask, l_mask))
    filtered_image = cv2.bitwise_and(image, image, mask=mask)
    print(f'H:{h_range}S:{s_range}:L{l_range}')
    return filtered_image


def convert_b64(image_cv2):
    encode_img = cv2.imencode('.jpg', image_cv2)
    b64_img = base64.b64encode(encode_img[1]).decode('utf-8')
    return b64_img


def main(page: ft.Page):
    image_path = "1-2.png"  # Replace with the actual path to your image
    original_image = cv2.imread(image_path)
    image_show = ft.Image(src_base64=convert_b64(original_image))

    def update_image(_):
        def str_to_int(value):
            return int(float(value))

        h_range = [str_to_int(h_slider.start_value), str_to_int(h_slider.end_value)]
        s_range = [str_to_int(s_slider.start_value), str_to_int(s_slider.end_value)]
        l_range = [str_to_int(l_slider.start_value), str_to_int(l_slider.end_value)]
        filtered_image = apply_hsl_filter(original_image, h_range, s_range, l_range)
        image_show.src_base64 = convert_b64(filtered_image)
        image_show.update()

    h_slider = ft.RangeSlider(min=0, max=180, start_value=0, end_value=180, divisions=181, label="{value} H",
                              on_change=update_image)
    s_slider = ft.RangeSlider(min=0, max=255, start_value=0, end_value=255, divisions=256, label="{value} S",
                              on_change=update_image)
    l_slider = ft.RangeSlider(min=0, max=255, start_value=0, end_value=255, divisions=256, label="{value} L",
                              on_change=update_image)

    # h_slider.on_change(update_image)
    # s_slider.on_change(update_image)
    # l_slider.on_change(update_image)

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                image_show,
                h_slider,
                s_slider,
                l_slider,
            ],
        )
    )


ft.app(target=main)
