import copy
import ctypes
from threading import Thread, Lock
from time import time, sleep

import numpy as np
import win32con
import win32gui
import win32ui
from mss import mss

user32 = ctypes.WinDLL('user32', use_last_error=True)


class WindowCapture:
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    stopped = True
    lock = None
    screenshot = None
    modifiedScreenshot = None

    def __init__(self, game_name, fps=False, imgGrab= False):
        self.imgGrab = imgGrab
        if self.imgGrab:
            self.sct = mss()
        #self.hwnd = "00110744"
        self.hwnd = win32gui.FindWindow(None, game_name)
        #win32gui.showWindow(self.hwnd, 4)
        win32gui.SetForegroundWindow(self.hwnd)
        print(self.hwnd)
        self.x, self.y, self.x1, self.y1 = win32gui.GetWindowRect(self.hwnd)

        self.fps = fps
        self.lock = Lock()
        self.h = self.y1 - self.y - 36
        self.w = self.x1 - self.x - 0
        print(self.x, self.y, self.w, self.h)
        self.cropped_y = 36
        self.cropped_x = 0
        self.offset_x = self.x + self.cropped_x
        self.offset_y = self.y + self.cropped_y
        self.center = {"x": round(self.w / 2), "y": round(self.h / 2)}

    def copy(self):
        return copy.deepcopy(self.screenshot)

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def coorAsList(self):
        return {"top": self.offset_y, "left": self.offset_x, "width": self.w, "height": self.h}

    def stop(self):
        self.stopped = True

    def run(self):
        loop_time = time()
        while not self.stopped:
            if not self.imgGrab:
                screenshot = self.getScreenshot()
            else:
                screenshot = self.getImgGrab()
            self.lock.acquire()
            self.screenshot = screenshot
            self.screenshot = self.copy()
            self.lock.release()
            sleep(0.01)
            if self.fps and time() - loop_time > 0:
                print('wc fps = {}/s'.format(1 / (time() - loop_time)))

            loop_time = time()

    def getImgGrab(self):
        return np.array(self.sct.grab(self.coorAsList()))[..., :3]

    def getScreenshot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDc = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDc.SelectObject(dataBitMap)
        cDc.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
        signedIntArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        dcObj.DeleteDC()
        cDc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[..., :3]
        img = np.ascontiguousarray(img)

        return img
