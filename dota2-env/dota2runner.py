import time

import pyautogui as gui


def run():
    launch_dota()
    set_timescale()
    start_game()


def launch_dota():
    gui.press('winleft')
    time.sleep(0.5)

    gui.typewrite('dota', interval=0.1)
    gui.press('enter')
    time.sleep(12.5)


def restart_game():
    time.sleep(3)
    gui.click(x=185, y=135, pause=1.5)
    gui.click(x=1555, y=975, pause=1.5)


def start_game():
    # start
    gui.click(x=1555, y=975, pause=0.3)
    # create lobby
    gui.click(x=1555, y=435, pause=1)
    # join coaches
    gui.click(x=1415, y=480, pause=3)
    # start game
    gui.click(x=1555, y=975, pause=0.5)


def set_timescale():
    gui.press('\\', pause=0.1)
    gui.typewrite('sv_cheats 1', interval=0.05, pause=0.3)
    gui.press('enter', pause=0.1)
    gui.typewrite('host_timescale 2', interval=0.05, pause=0.3)
    gui.press('enter', pause=0.1)
    gui.press('\\', pause=0.5)


if __name__ == '__main__':
    run()