
from flet import Page,CrossAxisAlignment,Container,Icon,icons,alignment,WindowDragArea,IconButton,Text,Row,MainAxisAlignment,app
from sys import path
path.append("./workbench")
import workbench.datas 
from workbench.mainwork import MainWork


def main(page: Page):
    page.window_title_bar_hidden = False
    page.window_frameless = True
    page.window_width = 300
    page.window_height = 380
    page.window_always_on_top=True

    page.bgcolor = "#240e13"
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.spacing = 30

    #输出GUI
    page.add(
        Row(
            [
                Container(padding=2),  #————调左边间距的
                Icon(icons.ADS_CLICK, color="#ffffff"),
                WindowDragArea(Container(Text("Limbug Clicker",color="#ffffff",size=23), padding=10), expand=True),
                IconButton(icons.CLOSE, on_click=lambda _: page.window_close(),icon_color="#ffffff",tooltip='close')
            ],
            
        ),
    )
    page.add(workbench.datas.img_Laetitia)
    page.add(
        Row(
            [   
                Container(Text("所",color="#c8c01a",size=60), padding=0,height=300,alignment=alignment.Alignment(-1, -1)),
                Container(Text("以,",color="#c8c01a",size=60), padding=0,height=300,alignment=alignment.Alignment(1, -0.7)),
                Container(Text("她 ",color="#e13317",size=90), padding=0,height=300,alignment=alignment.center),
                Container(Text("想出了这个绝妙的主意！！",color="#482d66",size=30), padding=0,height=300,width=100,alignment=alignment.Alignment(-0.5, -0.5)),
                workbench.datas.img_Monster,
                Container(Text("惊喜！！",color="#2f8c02",size=40), padding=10,height=300,width=100,alignment=alignment.Alignment(-10, -10)),
                Container(Text("礼物！！",color="#e13317",size=50), padding=10,height=300,width=100,alignment=alignment.Alignment(-10, -10)),
                Container(bgcolor="#ffffff",height=10,width=1000,alignment=alignment.Alignment(100, 100))
            ],
        alignment=MainAxisAlignment.CENTER,
        vertical_alignment=CrossAxisAlignment.CENTER,
        )
    )

    while True:
        MainWork()
        # time.sleep(0.1)
        # print("Waiting 0.1")    


app(target=main)