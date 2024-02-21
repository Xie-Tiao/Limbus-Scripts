import json
import logging
import os
import threading
import time

import flet as ft

import workbench


def main(page: ft.Page):
    page.window_title_bar_hidden = True
    page.window_frameless = True
    page.window_always_on_top = workbench.ui_config.ALWAYSE_ON_TOP
    page.window_width, page.window_height = workbench.ui_config.HOME_PAGE_SIZE
    page.spacing = 0
    page.theme = ft.theme.Theme(color_scheme_seed='red')

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
        route = e.control.data
        if route == '/home':
            pause_event.clear()
        else:
            pause_event.set()
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
            ft.dropdown.Option("日本語"),
            ft.dropdown.Option("한국어"),
        ],
        value=workbench.SettingsReader.read_option_language('Language', 'current'),
        label="Game Language",
        data={
            "English": 'en',
            "日本語": 'jp',
            "한국어": 'kr',
        },
        on_change=lambda e: workbench.SettingsReader.set_option('Language', 'Current', e.control.data[e.control.value]),
        content_padding=ft.padding.symmetric(horizontal=15),
    )
    # Log文件开关
    def log_button_changed(e):
        workbench.LoggingManager.toggle_logging(e.control.value)

    log_button = ft.Switch(label='Debug Logging', value=False, on_change=log_button_changed)
    
    # 置顶窗口开关
    def toggle_always_on_top():
        workbench.ui_config.ALWAYSE_ON_TOP = not workbench.ui_config.ALWAYSE_ON_TOP
        page.window_always_on_top = workbench.ui_config.ALWAYSE_ON_TOP
        return workbench.ui_config.ALWAYSE_ON_TOP

    window_always_on_top_button = ft.Switch(label='置顶窗口', value=True, on_change=lambda _: toggle_always_on_top())

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
        data=False, on_click=shortcut_record,
        bgcolor=workbench.ui_config.RECORD_BUTTON_COLOR
    )
    shortcut_button2 = ft.ElevatedButton(
        content=ft.Text(
            workbench.SettingsReader.read_option('Shortcut', 'shortcut2'),
            color=workbench.ui_config.RECORD_TEXT_COLOR
        ),
        data=False, on_click=shortcut_record,
        bgcolor=workbench.ui_config.RECORD_BUTTON_COLOR
    )
    button_list = [shortcut_button1, shortcut_button2]

    # 设置GUI
    view_settings = ft.View(
        route="/settings",
        bgcolor=ft.colors.GREY_200,
        appbar=ft.AppBar(
            title=ft.WindowDragArea(ft.Text("O-01-67")),
            leading=ft.IconButton(icon=ft.icons.ARROW_BACK, icon_size=20,on_click=switch_page, data="/home"),
            leading_width=45,
            toolbar_height=45,
            ),
        controls=[
            ft.Tabs(
                selected_index=0,
                animation_duration=200,
                scrollable=True,
                tabs=[
                    ft.Tab(
                        text="工作偏好",
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    # 顶部占位
                                    padding=1
                                ),
                                language_dropdown,
                                window_always_on_top_button,
                                # ft.Row(
                                #     alignment=ft.MainAxisAlignment.START,
                                #     controls=[
                                #     ft.Container(ft.Text("P键: ", weight=ft.FontWeight.W_600)),
                                #     shortcut_button1
                                # ]),
                                # ft.Row(
                                #     alignment=ft.MainAxisAlignment.START,
                                #     controls=[
                                #     ft.Container(ft.Text("Enter键: ", weight=ft.FontWeight.W_600)),
                                #     shortcut_button2
                                # ]),
                                ft.Container(
                                    # 底部占位
                                    padding=1
                                )
                            ],
                            scroll=ft.ScrollMode.ADAPTIVE,
                        )
                    ),
                    ft.Tab(
                        text="敏感信息",
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    # 顶部占位
                                    padding=1
                                ),
                                log_button,
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            spans=[
                                                ft.TextSpan(
                                                    "作者：协调人&Camreishi",
                                                    ft.TextStyle(weight=ft.FontWeight.BOLD)
                                                    ),
                                                
                                            ]
                                        ),
                                        ft.Text(
                                            spans=[
                                                ft.TextSpan("版本：4.0"),
                                            ]
                                        ),
                                        ft.Text(
                                            spans=[
                                                ft.TextSpan(
                                                    "github.com/Xie-Tiao/Limbus-Scripts",
                                                    ft.TextStyle(size=15)),
                                            ]
                                        ),
                                        ]
                                )
                            ],
                            scroll=ft.ScrollMode.ADAPTIVE,
                        ),
                    )
                ]
            )
            
        ],
    )
    views["/settings"] = view_settings

    pause_event = threading.Event()

    def pause_main_work(e):
        if pause_event.is_set():
            pause_event.clear()
            e.control.tooltip = '程序正在运行...'
            print("[Continue]")
        else:
            pause_event.set()
            e.control.tooltip = '⚠已暂停'
            print("[Pausing]")
        e.control.update()

    # 首页GUI
    # noinspection SpellCheckingInspection
    app_bar = ft.Container(
        padding=0,
        content=ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.ADS_CLICK,
                    icon_color="#ffffff",
                    on_click=switch_page,
                    data="/settings",
                    icon_size=20,
                    tooltip='设置',
                ),
                ft.WindowDragArea(
                    ft.Container(
                        ft.Text(
                            "Limbug Clicker",
                            color="#ffffff",
                            size=20,
                            no_wrap=False,
                            overflow="ellipsis",
                        ),
                    ),
                    expand=True,
                ),
                ft.IconButton(
                    icon=ft.icons.CLOSE,
                    on_click=lambda _: page.window_close(),
                    icon_color="#ffffff",
                    icon_size=20,
                    tooltip='close',
                )
            ],
        ),
    )

    assets_path = workbench.PathManager.ASSETS_RELPATH
    wich_image_path = os.path.join(assets_path, 'Wich', 'Wich_00000.png')
    img_Laetitia = ft.Image(
        src=wich_image_path,
        height=220,
        fit=ft.ImageFit.FIT_HEIGHT,
        gapless_playback=True
    )
    Laetitia = ft.WindowDragArea(
        ft.Container(
            alignment=ft.alignment.center,
            width=230,
            height=230,
            on_click=pause_main_work,
            tooltip = '程序正在运行...',
            ink=True,
            content=img_Laetitia
        ))

    Monster = ft.Row(
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

    view_home.controls.append(app_bar)
    view_home.controls.append(Laetitia)
    view_home.controls.append(Monster)

    page.views.append(views["/home"])
    page.update()

    def Laetitia_Animation(i):
        # print(i)
        wich_image_path = os.path.join(assets_path, 'Wich', f'Wich_{i:05}.png')
        img_Laetitia.src = wich_image_path
        try:
            Laetitia.update()
        except AssertionError:
            pass
        time.sleep(0.1)

    def animation_thread(pause_event):
        idx = 0
        while True:
            if not pause_event.is_set():
                Laetitia_Animation(idx)
                idx += 1
                idx = idx % 24
            else:
                pass

    def main_thread(pause_event):
        while True:
            if not pause_event.is_set():
                workbench.mission_handling.main()
            else:
                pass
            time.sleep(0.1)

    # 创建两个线程
    animation_t = threading.Thread(target=animation_thread, args=(pause_event,))
    main_t = threading.Thread(target=main_thread, args=(pause_event,))

    # 启动线程
    animation_t.start()
    main_t.start()

    # 等待线程结束
    animation_t.join()
    main_t.join()


if __name__ == '__main__':
    # noinspection PyBroadException
    try:
        ft.app(target=main)

    except Exception:
        logging.exception("An error occurred: ")
