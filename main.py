from threading import Event

import flet as ft

import workbench.datas
from workbench.mainwork import main_work


def main(page: ft.Page):
    page.window_width = 260
    page.window_height = 340
    page.window_title_bar_hidden = True
    page.window_frameless = True
    page.window_always_on_top = True
    # page.padding=0
    # page.margin=0

    page.bgcolor = "#240e13"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.spacing = 30

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
            
    is_paused = False

    def toggle_icon(e):
        nonlocal is_paused
        is_paused = not is_paused
        if is_paused:
            # e.control.icon = ft.icons.REPLAY
            e.control.tooltip = '⚠已暂停'
        else:
            # e.control.icon = ft.icons.ADS_CLICK
            e.control.tooltip = '程序正在运行...' 
        e.control.update()
        pause_main_work()

    

    # 输出GUI
    page.add(
        ft.Container(
            # padding=ft.padding.symmetric(horizontal=5),
            content=ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.SETTINGS_ROUNDED, 
                        icon_color="#ffffff", 
                        icon_size=20,
                        tooltip='设置',
                    ),
                    ft.WindowDragArea(
                        ft.Container(
                            ft.Text(
                                "Limbug Clicker",
                                color="#ffffff", 
                                size=20,
                                # weight=ft.FontWeight.W_500,
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
    )
    page.add(
        ft.Container(
            image_src="./assets/Wich.webp",
            alignment=ft.alignment.center,
            width=230,
            height=230,
            on_click=toggle_icon, 
            ink=True,
            # content=ft.Image(
            #     src="./assets/Wich.webp", 
            #     height=230, 
            #     fit=ft.ImageFit.FIT_HEIGHT, 
            #     tooltip="程序正在运行...",
            # )
        )
    )
    page.add(
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
                workbench.datas.img_Monster,
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

    while True:
        if not pause_event.is_set():

            main_work()
        else:
            pass


if __name__ == '__main__':
    ft.app(target=main)
