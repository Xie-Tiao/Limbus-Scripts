import flet as ft

import workbench


def main(page: ft.Page):
    def handle_route_change(r: ft.RouteChangeEvent):
        if page.route == "/settings":
            page.views.clear()
            page.views.append(views["/settings"])

        elif page.route == "/home":
            page.views.clear()
            page.views.append(views["/home"])

    def go_settings(e: ft.ControlEvent):
        page.go("/settings")

    def go_home(e: ft.ControlEvent):
        page.go("/home")

    page.title = "Settings Navigation Example"
    page.horizontal_alignment = page.vertical_alignment = "center"
    views = workbench.ui_config.views

    views["/settings"] = ft.View(
        route="/settings",
        fullscreen_dialog=True,
        appbar=ft.AppBar(
            title=ft.Text("Settings Page"),
            leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_home)),
        controls=[ft.Text("Settings Content", weight=ft.FontWeight.BOLD, size=20)]
    )
    views["/home"] = ft.View(
        route="/home",
        controls=[ft.OutlinedButton("Go to Settings", on_click=go_settings)]
    )

    page.on_route_change = handle_route_change
    # page.on_view_pop = handle_view_pop
    page.add(
        ft.OutlinedButton("Go to Settings", on_click=go_settings)
    )


ft.app(target=main)
