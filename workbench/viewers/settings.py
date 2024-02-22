import flet as ft
import time
import json

from workbench import SettingsReader,LoggingManager,ui_config

# /settings

# 创建一个下拉框，用于选择游戏语言
language_dropdown = ft.Dropdown(
    options=[
        ft.dropdown.Option("English"),
        ft.dropdown.Option("日本語"),
        ft.dropdown.Option("한국어"),
    ],
    value=SettingsReader.read_option_language('Language', 'current'),
    label="Game Language",
    data={
        "English": 'en',
        "日本語": 'jp',
        "한국어": 'kr',
    },
    on_change=lambda e: SettingsReader.set_option('Language', 'Current', e.control.data[e.control.value]),
    content_padding=ft.padding.symmetric(horizontal=15),
)

# Log文件开关
def log_button_changed(e):
    LoggingManager.toggle_logging(e.control.value)

log_button = ft.Switch(label='Debug Logging', value=False, on_change=log_button_changed)

# 置顶窗口开关
def toggle_always_on_top():
    ui_config.ALWAYSE_ON_TOP = not ui_config.ALWAYSE_ON_TOP
    ft.Page.window_always_on_top = ui_config.ALWAYSE_ON_TOP
    return ui_config.ALWAYSE_ON_TOP

window_always_on_top_button = ft.Switch(label='置顶窗口', value=True, on_change=lambda _: toggle_always_on_top())

def shortcut_record(e):
    button = e.control
    button.data = True
    button.content.color = ft.colors.WHITE
    button.content.value = "Recording..."
    button.bgcolor = ui_config.MAIN_COLOR
    button.update()

# 创建两个按钮，用于设置快捷键
shortcut_button1 = ft.ElevatedButton(
    content=ft.Text(
        SettingsReader.read_option('Shortcut', 'shortcut1'),
        color=ui_config.RECORD_TEXT_COLOR
    ),
    data=False, on_click=shortcut_record,
    bgcolor=ui_config.RECORD_BUTTON_COLOR
)
shortcut_button2 = ft.ElevatedButton(
    content=ft.Text(
        SettingsReader.read_option('Shortcut', 'shortcut2'),
        color=ui_config.RECORD_TEXT_COLOR
    ),
    data=False, on_click=shortcut_record,
    bgcolor=ui_config.RECORD_BUTTON_COLOR
)
button_list = [shortcut_button1, shortcut_button2]

def on_keyboard(e: ft.KeyboardEvent):
    # print(e.key)
    for i in range(len(button_list)):
        button = button_list[i]
        if button.data:
            data = json.loads(e.data)  # 转换 string 到 dictionary
            keys_pressed = [k for k, v in data.items() if v and k != 'key']

            button.content.value = ' + '.join(keys_pressed + [data['key']])
            SettingsReader.set_option('Shortcut', f'shortcut{i + 1}', button.content.value)
            button.data = False

            button.update()

            time.sleep(0.3)
            button.content.color = ui_config.RECORD_TEXT_COLOR
            button.bgcolor = ui_config.RECORD_BUTTON_COLOR
            ft.Page.update()

            break

ft.Page.on_keyboard_event = on_keyboard

# 关于
about = ft.Column(
    # expand=1,
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
                    ft.TextStyle(size=10, color=ui_config.RECORD_TEXT_COLOR, weight=ft.FontWeight.W_900),
                    url="https://github.com/Xie-Tiao/Limbus-Scripts",
                ),
                ft.TextSpan(
                    " | ",
                    ft.TextStyle(weight=ft.FontWeight.BOLD)
                ),
                ft.TextSpan(
                    "版本：4.0.0",
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
        leading=ft.IconButton(icon=ft.icons.ARROW_BACK, icon_size=20,  data="/home"),
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
                    content=ft.Column(
                        scroll=ft.ScrollMode.ADAPTIVE,
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
                            log_button,
                            ft.Container(expand=1),
                            ft.Divider(),
                            about,
                            # ft.Container(expand=1, bgcolor=ft.colors.RED),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
            ]
        )

    ],
)
views = ui_config.views
views["/settings"] = view_settings