import logging
import os
import threading
import time

import flet as ft

import workbench


def main(page: ft.Page):
    page.window_title_bar_hidden = True
    page.window_frameless = True
    page.window_always_on_top = workbench.ui_config.ALWAYS_ON_TOP
    page.window_width, page.window_height = workbench.ui_config.HOME_PAGE_SIZE
    page.spacing = 0
    page.theme = ft.theme.Theme(color_scheme_seed='red')
    page.window_bgcolor = ft.colors.TRANSPARENT

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
        # if route == '/home':
        #     pause_event.clear()
        #     print("[Continue]")
        # else:
        #     pause_event.set()
        #     print("[Pausing]")
        page.go(route)

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

    # /settings

    # 创建一个下拉框，用于选择游戏语言
    language_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("零协汉化"),
            ft.dropdown.Option("English"),
            ft.dropdown.Option("日本語"),
            ft.dropdown.Option("한국어"),
        ],
        value=workbench.SettingsReader.read_option_language('Language', 'current'),
        label="Game Language",
        data={
            "零协汉化":'zh',
            "English": 'en',
            "日本語": 'jp',
            "한국어": 'kr',
        },
        on_change=lambda e: workbench.SettingsReader.set_option('Language', 'Current', e.control.data[e.control.value]),
        content_padding=ft.padding.symmetric(horizontal=15),
    )

    # 置顶窗口开关
    def toggle_always_on_top():
        workbench.ui_config.ALWAYS_ON_TOP = not workbench.ui_config.ALWAYS_ON_TOP
        page.window_always_on_top = workbench.ui_config.ALWAYS_ON_TOP
        return workbench.ui_config.ALWAYS_ON_TOP

    window_always_on_top_button = ft.Switch(label='置顶开关', value=True, on_change=lambda _: toggle_always_on_top())

    # ego开关
    def toggle_ego():
        if workbench.SettingsReader.read_option('EGO', 'value') == 'True':
            workbench.SettingsReader.set_option('EGO', 'value', 'False')
        else:
            workbench.SettingsReader.set_option('EGO', 'value', 'True')

    ego_button = ft.Switch(label='ego开关', value=workbench.SettingsReader.read_option('EGO', 'value'),
                           on_change=lambda _: toggle_ego())
    
    # 阵亡重开开关
    def toggle_death():
        if workbench.SettingsReader.read_option('DEATH', 'value') == 'True':
            workbench.SettingsReader.set_option('DEATH', 'value', 'False')
        else:
            workbench.SettingsReader.set_option('DEATH', 'value', 'True')

    death_button = ft.Switch(label='阵亡重开', value=workbench.SettingsReader.read_option('DEATH', 'value'),
                           on_change=lambda _: toggle_death())

    # 桌宠模式开关
    def toggle_pet():
        if workbench.SettingsReader.read_option('OPACITY', 'opacity') == '1':
            workbench.SettingsReader.set_option('OPACITY', 'opacity', '0')
            workbench.SettingsReader.set_option('OPACITY', 'value', 'True')
        else:
            workbench.SettingsReader.set_option('OPACITY', 'opacity', '1')
            workbench.SettingsReader.set_option('OPACITY', 'value', 'False')

    pet_button = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Switch(label='桌宠模式', value=workbench.SettingsReader.read_option('OPACITY', 'value'),
                      on_change=lambda _: toggle_pet()),
            ft.Text(
                "—— 设置桌宠请重启 ——",
                size=12,
            )
        ]
    )

    # 关于
    about = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                size=13,
                weight=ft.FontWeight.W_400,
                spans=[
                    ft.TextSpan(
                        "作者: ",
                    ),
                    ft.TextSpan(
                        "协调人",
                        url="https://github.com/Xie-Tiao",
                    ),
                    ft.TextSpan(
                        " & ",
                    ),
                    ft.TextSpan(
                        "Camreishi",
                        url="https://github.com/Camreishi",
                    ),
                ]
            ),
            ft.Text(
                spans=[
                    ft.TextSpan(
                        "开源仓库",
                        ft.TextStyle(size=10, color=workbench.ui_config.RECORD_TEXT_COLOR, weight=ft.FontWeight.W_900),
                        url="https://github.com/Xie-Tiao/Limbus-Scripts",
                    ),
                    ft.TextSpan(
                        " | ",
                        ft.TextStyle(weight=ft.FontWeight.BOLD)
                    ),
                    ft.TextSpan(
                        "版本：4.1.0",
                        ft.TextStyle(size=10, weight=ft.FontWeight.W_900),
                    ),
                ]
            ),
        ]
    )

    # 设置GUI
    view_settings = ft.View(
        route="/settings",
        bgcolor=ft.colors.GREY_200,
        appbar=ft.AppBar(
            title=ft.WindowDragArea(ft.Text("O-01-67")),
            leading=ft.IconButton(icon=ft.icons.ARROW_BACK, icon_size=20, on_click=switch_page, data="/home"),
            leading_width=45,
            toolbar_height=45,
        ),
        padding=0,
        controls=[
            ft.Tabs(
                selected_index=0,
                animation_duration=200,
                scrollable=True,
                tab_alignment=ft.TabAlignment.CENTER,
                expand=True,
                tabs=[
                    ft.Tab(
                        # text="工作偏好",
                        tab_content=ft.Text('工作偏好', width=68, text_align=ft.TextAlign.CENTER),
                        content=ft.Container(
                            padding=12,
                            content=ft.Column(
                                scroll=ft.ScrollMode.AUTO,
                                controls=[
                                    ft.Container(
                                        # 顶部占位
                                        padding=1
                                    ),
                                    language_dropdown,
                                    window_always_on_top_button,
                                    ego_button,
                                    death_button,
                                    ft.Container(
                                        # 底部占位
                                        padding=1
                                    )
                                ],
                            )
                        )
                    ),
                    ft.Tab(
                        # text="敏感信息",
                        tab_content=ft.Text('敏感信息', width=68, text_align=ft.TextAlign.CENTER),
                        content=ft.Column(
                            # scroll=ft.ScrollMode.ADAPTIVE,
                            controls=[
                                ft.Container(
                                    # 顶部占位
                                    padding=1
                                ),
                                ft.Container(
                                    padding=10,
                                    content=ft.Column(
                                        controls=[
                                            pet_button,
                                        ]
                                    )
                                ),
                                ft.Container(expand=1),
                                ft.Divider(),
                                about,
                                ft.Container(
                                    # 底部占位
                                    padding=1
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    )
                ]
            )

        ],
    )

    app_bar = ft.Container(
        opacity=workbench.SettingsReader.read_option('OPACITY', 'opacity'),
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

    # 首页GUI
    # noinspection SpellCheckingInspection

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
            tooltip='程序正在运行...',
            ink=True,
            content=img_Laetitia
        ))

    img_Monster = ft.Image(
        src=os.path.join(assets_path, 'LaetitiaMinionCrop.webp'),
        width=800,
        fit=ft.ImageFit.FIT_WIDTH
    )

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
            img_Monster,
            ft.Container(ft.Text("惊喜！！", color="#2f8c02", size=40), padding=10, height=300, width=100,
                         alignment=ft.alignment.Alignment(-10, -10)),
            ft.Container(ft.Text("礼物！！", color="#e13317", size=50), padding=10, height=300, width=100,
                         alignment=ft.alignment.Alignment(-10, -10)),
            ft.Container(bgcolor="#ffffff", height=10, width=1000, alignment=ft.alignment.Alignment(100, 100))
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # /home
    view_home = ft.View(
        route="/home",
        bgcolor=ft.colors.with_opacity(workbench.SettingsReader.read_option('OPACITY', 'opacity'),
                                       workbench.ui_config.MAIN_COLOR),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            app_bar,
            Laetitia,
            Monster
        ]
    )

    views = workbench.ui_config.views
    views["/settings"] = view_settings
    views["/home"] = view_home
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
                workbench.main_work.main()
            else:
                pass

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
