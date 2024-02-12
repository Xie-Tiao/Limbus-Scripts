import json
import logging
import time
from threading import Event

import flet as ft

import workbench


def main(page: ft.Page):
    page.window_title_bar_hidden = True
    page.window_frameless = True
    page.window_width, page.window_height = workbench.ui_config.HOME_PAGE_SIZE
    page.window_always_on_top = True
    page.theme = ft.theme.Theme(color_scheme_seed='red')
    page.spacing = 30

    # logger = workbench.LoggingManager.logger
    # logger.info('123')

    def handle_route_change(_):
        if page.route == "/settings":
            page.window_width, page.window_height = workbench.ui_config.SETTING_PAGE_SIZE
            page.views.clear()
            page.views.append(views["/settings"])

        elif page.route == "/home":
            # save settings.ini when return home
            workbench.SettingsReader.write_config()
            page.window_width, page.window_height = workbench.ui_config.HOME_PAGE_SIZE
            page.views.clear()
            page.views.append(views["/home"])

    page.on_route_change = handle_route_change

    def switch_page(e):
        pause_main_work()
        route = e.control.data
        workbench.keyboard_control.keyboard.press_keys('shift')
        page.go(route)

    def on_keyboard(e: ft.KeyboardEvent):
        # print(e.key)
        for i in range(len(button_list)):
            button = button_list[i]
            if button.data:
                data = json.loads(e.data)  # 转换 string 到 dictionary
                keys_pressed = [k for k, v in data.items() if v and k != 'key']

                button.content.value = ' + '.join(keys_pressed + [data['key']])
                workbench.SettingsReader.set_option('Shortcut', f'shortcut{i + 1}', button.content.value)
                button.data = False

                button.update()

                time.sleep(0.3)
                button.content.color = workbench.ui_config.RECORD_TEXT_COLOR
                button.bgcolor = workbench.ui_config.RECORD_BUTTON_COLOR
                page.update()

                break

    page.on_keyboard_event = on_keyboard

    views = workbench.ui_config.views
    # /home
    view_home = ft.View(
        route="/home",
        bgcolor=workbench.ui_config.MAIN_COLOR,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    views["/home"] = view_home

    # /settings
    # 创建一个下拉框，用于选择游戏语言

    language_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("English"),
            ft.dropdown.Option("Japanese"),
            ft.dropdown.Option("Korean"),
        ],
        value=workbench.SettingsReader.read_option('Language', 'current'),
        label="Game Language",
        on_change=lambda e: workbench.SettingsReader.set_option('Language', 'Current', e.control.value)
    )

    def log_button_changed(e):
        workbench.LoggingManager.toggle_logging(e.control.value)

    log_button = ft.Switch(label='Debug Logging', value=False, on_change=log_button_changed)

    def shortcut_record(e):
        button = e.control
        button.data = True
        button.content.color = ft.colors.WHITE
        button.content.value = "Recording..."
        button.bgcolor = workbench.ui_config.MAIN_COLOR
        button.update()

    # 创建两个按钮，用于设置快捷键
    shortcut_button1 = ft.ElevatedButton(
        content=ft.Text(
            workbench.SettingsReader.read_option('Shortcut', 'shortcut1'),
            color=workbench.ui_config.RECORD_TEXT_COLOR
        ),
        width=200,
        data=False, on_click=shortcut_record,
        bgcolor=workbench.ui_config.RECORD_BUTTON_COLOR
    )
    shortcut_button2 = ft.ElevatedButton(
        content=ft.Text(
            workbench.SettingsReader.read_option('Shortcut', 'shortcut2'),
            color=workbench.ui_config.RECORD_TEXT_COLOR
        ),
        width=200,
        data=False, on_click=shortcut_record,
        bgcolor=workbench.ui_config.RECORD_BUTTON_COLOR
    )
    button_list = [shortcut_button1, shortcut_button2]
    view_settings = ft.View(
        route="/settings",
        bgcolor=ft.colors.GREY_200,
        appbar=ft.AppBar(
            title=ft.Text("Settings"),
            leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=switch_page, data="/home")),
        controls=[
            language_dropdown,
            log_button,
            ft.Row(controls=[
                ft.Container(width=10),
                ft.Text("Shortcut 1: "),
                shortcut_button1
            ]),
            ft.Row(controls=[
                ft.Container(width=10),
                ft.Text("Shortcut 2: "),
                shortcut_button2
            ]),
        ]
    )
    views["/settings"] = view_settings

    pause_event = Event()

    def pause_main_work():
        if pause_event.is_set():
            # Already paused, resume the process
            pause_event.clear()
            print("[Continue]")
        else:
            # Pause the process
            pause_event.set()
            print("[Pausing]")

    # 输出GUI
    # noinspection SpellCheckingInspection
    view_home.controls.append(
        ft.Row(
            [
                # ft.Container(padding=2),  # ————调左边间距的
                ft.IconButton(ft.icons.ADS_CLICK, icon_color="#ffffff", on_click=lambda _: pause_main_work(),
                              tooltip='stop'),
                ft.WindowDragArea(ft.Container(ft.Text("Limbug Clicker", color="#ffffff", size=20)),
                                  expand=True),
                ft.IconButton(ft.icons.SETTINGS, on_click=switch_page, icon_color="#ffffff",
                              tooltip='settings', data="/settings"),
                ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close(), icon_color="#ffffff",
                              tooltip='close')
            ],

        ),
    )
    view_home.controls.append(workbench.ui_config.img_Laetitia)
    view_home.controls.append(
        ft.Row(
            [
                ft.Container(ft.Text("所", color="#c8c01a", size=60), padding=0, height=300,
                             alignment=ft.alignment.Alignment(-1, -1)),
                ft.Container(ft.Text("以,", color="#c8c01a", size=60), padding=0, height=300,
                             alignment=ft.alignment.Alignment(1, -0.7)),
                ft.Container(ft.Text("她 ", color="#e13317", size=90), padding=0, height=300,
                             alignment=ft.alignment.center),
                ft.Container(ft.Text("想出了这个绝妙的主意！！", color="#482d66", size=30), padding=0, height=300,
                             width=100,
                             alignment=ft.alignment.Alignment(-0.5, -0.5)),
                workbench.ui_config.img_Monster,
                ft.Container(ft.Text("惊喜！！", color="#2f8c02", size=40), padding=10, height=300, width=100,
                             alignment=ft.alignment.Alignment(-10, -10)),
                ft.Container(ft.Text("礼物！！", color="#e13317", size=50), padding=10, height=300, width=100,
                             alignment=ft.alignment.Alignment(-10, -10)),
                ft.Container(bgcolor="#ffffff", height=10, width=1000, alignment=ft.alignment.Alignment(100, 100))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    page.views.append(views["/home"])
    page.update()

    while True:
        if not pause_event.is_set():
            # workbench.mission_handling.main()
            # workbench.mission_handling.test()
            # workbench.mission_handling.test_ocr()
            workbench.mission_handling.test_choices()
            # logger.info('321')

        else:
            pass
        time.sleep(0.2)


if __name__ == '__main__':
    # noinspection PyBroadException
    try:
        ft.app(target=main)

    except Exception:
        logging.exception("An error occurred: ")
