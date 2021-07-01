from time import sleep

import win32com.client

from gameClass.action import Action
from gameClass.game import Game
from util.DataPickController import ImageDataPickerController
from util.jsonfunction import *
from util.windowcapture import WindowCapture
import cv2
import numpy as np

img = None


def pick_color(event, x, y, flags, param):
    global img
    img = img[..., :3]
    if event == cv2.EVENT_LBUTTONDOWN:
        if img is not None:
            pixel = img[y, x]
            # you might want to adjust the ranges(+-10, etc):
            upper = np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 20])
            lower = np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 20])
            print("----\nx: {}\ny: {}\npixel: {}\nlower: {}\nupper: {}".format(x, y,
                                                                         "[" + ", ".join(str(v) for v in pixel) + "]",
                                                                         "[" + ", ".join(str(v) for v in lower) + "]",
                                                                         "[" + ", ".join(str(v) for v in upper) + "]"))

            image_mask = cv2.inRange(img, lower, upper)
            cv2.imshow("mask", image_mask)


def main():
    global img
    gameName = "Pixel Starships"
    windowCopyName = gameName + " copy"  # the screen copyed
    windowDrawName = gameName + " draw"  # the screen drawed
    stopped = False
    screenshot = None

    shell = win32com.client.Dispatch("WScript.Shell")
    shell.AppActivate(gameName)

    screenPosition = getJson("json/screenPosition.json")
    dataPickData = getJson("json/dataPick.json")
    print("sP",screenPosition)

    wc = WindowCapture(gameName, imgGrab=True)
    action = Action((wc.offset_x, wc.offset_y), wc.center, screenPosition)
    dpc = ImageDataPickerController(wc, dataPickData)
    game = Game(wc, dpc, action, dataPickData, screenPosition)

    wc.start()
    dpc.start()
    game.start()

    cv2.namedWindow(windowCopyName)
    if dpc.draw:
        cv2.namedWindow(windowDrawName)

    cv2.setMouseCallback(windowCopyName, pick_color)

    while not stopped:
        if wc.screenshot is not None:  # show img cpy
            screenshot = wc.screenshot
            img = wc.copy()
            cv2.imshow(windowCopyName, screenshot)
        if dpc.draw and dpc.screenshotOut is not None:  ## show drawed img
            cv2.imshow(windowDrawName, dpc.screenshotOut)

        key = cv2.waitKey(1)
        if key == ord('q'):  # quit
            wc.stop()
            dpc.stop()
            game.stop()
            stopped = True
        if key == ord('s'):  # save img
            if screenshot is not None:
                cv2.imwrite("./tmp/main.png", screenshot)
        if key == ord("p"):
            game.startPvp()
        sleep(0.01)


if __name__ == '__main__':
    main()
