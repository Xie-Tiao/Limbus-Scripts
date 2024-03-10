import pyautogui as pg
import file_path_utils
import json
import os
import time
pg.FAILSAFE = False
# 界面检查模块
def check_img(img, confid=0.9):
    try:
        if pg.locateOnScreen(file_path_utils.PathManager.get_local_image(img), confidence=confid) is not None:
            print('看到了...', img)
            return True
    except pg.ImageNotFoundException:
        print('没看到..', img)
        return False


def check_img_list(img_list, confid=0.9):
    for i in range(len(img_list)):
        if check_img(img_list[i], confid):
            return True
    return False

# 控制模块
def mouse_click(img, times=1, confid=0.9):
    try:
        location = pg.locateCenterOnScreen(file_path_utils.PathManager.get_local_image(img), confidence=confid)
        if location is not None:
            pg.click(
                location.x,
                location.y,
                interval=0.6,
                duration=0,
                clicks=times,
                button='left',
            )
            pg.moveTo(0, 0)
            print("点到了 ...", img)
    except pg.ImageNotFoundException:
        print("没点到 ...", img)


def mouse_click_img_list(img_list, times=1, confid=0.9):
    for i in range(len(img_list)):
        if mouse_click(img_list[i], times, confid):
            return True
    return False

_worklist_path = os.path.join(file_path_utils.PathManager.CURRENT_DIR, 'worklist.json')
with open(_worklist_path, 'r', encoding='utf-8') as f:
    _worklist = json.load(f)

##————————————————————————————————————————————
##————————————————————————————————————————————
def start_mirror():
    mouse_click_img_list(_worklist['start_mirror'])

def end_mirror():
    mouse_click_img_list(_worklist['end_mirror'])

def gift(camp):
    for _ in range(2):
        camp_checked = check_img_list(_worklist[f'{camp}_checked'][0],0.85) & check_img_list(_worklist[f'{camp}_checked'][1],0.85)
        if camp_checked:
            mouse_click_img_list(_worklist[f'{camp}_click'],confid=0.85)
            mouse_click('gifts_checked_1690.png')
            print('等待下一步操作')
            time.sleep(999999)
        else:
            mouse_click('refresh_1690.png')

def mirror_opening_field():
    while True:
        start_mirror()
        gift('bleed')
        end_mirror()

"""
    流血: bleed
    呼吸: breath
    烧伤: burn
    破裂: fracture

"""

if __name__ == '__main__':
    mirror_opening_field()
