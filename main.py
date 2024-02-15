import threading
import time
import flet as ft

import workbench.datas
from workbench.mainwork import main_work
from PIL import Image, ImageTk
import os

def main(page: ft.Page):
    page.window_width = 200
    page.window_height = 300
    page.window_title_bar_hidden = True
    page.window_frameless = True
    page.window_always_on_top = True
    # page.padding=0
    page.margin=0
    page.spacing=0

    page.bgcolor = "#240e13"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    pause_event = threading.Event()
    
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
    AppBar = ft.Container(
            padding=0,
            content=ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.ADS_CLICK, 
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
    
    wich_image_path = os.path.join('assets', 'Wich', 'Wich_00000.png')

    img_Laetitia=ft.Image(
                    src=wich_image_path,
                    height=220,
                    fit=ft.ImageFit.FIT_HEIGHT,
                    gapless_playback=True
                )
    
    Laetitia=ft.WindowDragArea(
        ft.Container(
                alignment=ft.alignment.center,
                width=230,
                height=230,
                # margin=ft.margin.only(bottom=10),
                on_click=toggle_icon, 
                ink=True,
                content=img_Laetitia
    ))

    # Laetitia = ft.WindowDragArea(
    #         ft.Container(
    #             alignment=ft.alignment.center,
    #             width=230,
    #             height=230,
    #             # margin=ft.margin.only(bottom=10),
    #             on_click=toggle_icon, 
    #             ink=True,
    #             content=ft.Image(
    #                 src="./assets/Wich.webp", 
    #                 height=220, 
    #                 fit=ft.ImageFit.FIT_HEIGHT, 
    #             )
    #         )
    #     )
    
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
    
    page.add(AppBar,Laetitia, Monster)

    def Laetitia_Animation(i):
        print(i)
        wich_image_path = os.path.join('assets', 'Wich', f'Wich_{i:05}.png')
        img_Laetitia.src = wich_image_path
        Laetitia.update()
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
                    main_work()
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
    ft.app(target=main)