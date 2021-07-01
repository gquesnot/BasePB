from threading import Thread
from time import sleep

import cv2

from util.baseDataPick import BaseImageDataPicker
from util.jsonfunction import *
from util.threadclass import ThreadClass


class ImageDataPickerController(ThreadClass):
    def __init__(self, wc, inputDatas):
        super().__init__()
        self.screenshotIn = None
        self.screenshotOut = None
        self.inputDatas = inputDatas
        self.wc = wc
        self.draw = False
        self.outputDatas = {}
        for key, elem in self.inputDatas.items():
            self.outputDatas[key] = BaseImageDataPicker(self, key, elem['datas'], draw=elem['draw'])
            if self.outputDatas[key].draw:
                self.draw = True

    def start(self):
        if self.draw:
            self.stopped = False
            t = Thread(target=self.run)
            t.start()

    def getAllCoors(self):
        return {key: val.getCoors() for key, val in self.outputDatas.items()}

    def getAllContours(self):
        return {key: val.getContours() for key, val in self.outputDatas.items()}

    def getScreenshot(self):
        return self.screenshotOut

    def stop(self):
        super().stop()

    def run(self):
        while not self.stopped:
            self.drawAll()
            sleep(0.01)

    def hasCoors(self, group, elemName):
        return True if len(self.outputDatas[group].results[elemName]['coors']) > 0 else False

    def getCoors(self, group, elemName):
        return self.outputDatas[group].results[elemName]['coors']

    def drawAll(self):
        screenshot = self.wc.copy()
        for key, elem in self.outputDatas.items():
            if elem.draw:
                for k, contours in elem.getContours().items():
                    if len(contours) > 0:
                        cv2.drawContours(screenshot, contours, -1, elem.inputDatas[k]['drawColor'], 3)
        self.screenshotOut = screenshot
