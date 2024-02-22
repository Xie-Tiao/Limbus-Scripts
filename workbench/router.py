from flet import Page as page
from . import ui_config
from workbench import SettingsReader
from viewers import view_home, view_settings

views = ui_config.views
views["/home"] = view_home
views["/settings"] = view_settings


def handle_route_change(_):
    if page.route == "/settings":
        page.window_width, page.window_height = ui_config.SETTING_PAGE_SIZE
        page.views.clear()
        page.views.append(views["/settings"])

    elif page.route == "/home":
        # save settings.ini when return home
        SettingsReader.write_config()
        page.window_width, page.window_height = ui_config.HOME_PAGE_SIZE
        page.views.clear()
        page.views.append(views["/home"])