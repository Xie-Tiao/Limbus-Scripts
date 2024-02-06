import json
import time

import flet
from flet import Container, Page, Row, Text, border, colors, KeyboardEvent


class ButtonControl(Container):
    def __init__(self, text):
        super().__init__()
        self.content = Text(text)
        self.border = border.all(1, colors.BLACK54)
        self.border_radius = 3
        self.bgcolor = "0x09000000"
        self.padding = 10
        self.visible = False


def main(page: Page):
    def on_keyboard(e: KeyboardEvent):
        # for attr, value in vars(e).items():
        #     print(f"{attr}: {value}")
        data = json.loads(e.data)  # 转换 string 到 dictionary
        keys_pressed = [k for k, v in data.items() if v and k != 'key']
        final_string = ' + '.join(keys_pressed + [data['key']])
        print(final_string)

        key.content.value = e.key
        key.visible = True
        shift.visible = e.shift
        ctrl.visible = e.ctrl
        alt.visible = e.alt
        meta.visible = e.meta
        page.update()
        time.sleep(0.5)
        key.visible = False
        shift.visible = False
        ctrl.visible = False
        alt.visible = False
        meta.visible = False
        page.update()

    page.on_keyboard_event = on_keyboard

    key = ButtonControl("")
    shift = ButtonControl("Shift")
    ctrl = ButtonControl("Control")
    alt = ButtonControl("Alt")
    meta = ButtonControl("Meta")

    page.spacing = 50
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.add(
        Text("Press any key with a combination of CTRL, ALT, SHIFT and META keys..."),
        Row([key, shift, ctrl, alt, meta], alignment="center"),
    )


flet.app(target=main)
