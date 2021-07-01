import copy
import json
from abc import abstractmethod
from time import time, sleep

import cv2
import numpy as np

from util.threadclass import ThreadClass


class BaseImageDataPicker(ThreadClass):
    screenshot = None
    modifiedScreenshot = None
    results = {}
    loop_time = None
    fps = False

    def __init__(self, imageDataPicker, name, datas, draw=False, fps=False):
        super().__init__()
        self.dpc = imageDataPicker
        self.name = name
        self.draw = draw
        self.kernal = np.ones((5, 5), "uint8")
        self.inputDatas = datas

        for key, elem in self.inputDatas.items():
            self.inputDatas[key]['lowerMask'] = np.array(elem['lower'], np.uint8)
            self.inputDatas[key]['upperMask'] = np.array(elem['upper'], np.uint8)
            self.results[key] = {"contours": [], "coors": []}
        self.start()


    # def drawResult(self):
    #     for key in self.outputDatas.keys() & self.inputDatas.keys():
    #         outputData = self.outputDatas[key]
    #         inputData = self.inputDatas[key]
    #         for elem in outputData['result']:
    #             print("x: {}, y: {}, width: {}, height: {}".format(elem[0][0], elem[0][1], elem[1][0] - elem[0][0], elem[1][1] - elem[0][1]))

    def applyConditions(self, datas, conditions):

        for condition in conditions:
            if condition[1] == ">":
                if not datas[condition[0]] > condition[2]:
                    return False
            elif condition[1] == ">=":
                if not datas[condition[0]] >= condition[2]:
                    return False
            elif condition[1] == "<":
                if not datas[condition[0]] < condition[2]:
                    return False
            elif condition[1] == "<=":
                if not datas[condition[0]] <= condition[2]:
                    return False
            elif condition[1] == "==":
                if not datas[condition[0]] == condition[2]:
                    return False
        return True

    def getCoors(self):
        return {key: val['coors'] for key, val in self.results.items()}

    def getContours(self):
        return {key: val['contours'] for key, val in self.results.items()}

    def scanDatas(self):
        screenshot = self.dpc.wc.screenshot
        if screenshot is not None:
            for key, elem in self.inputDatas.items():

                mask =  cv2.inRange(screenshot, elem['lowerMask'], elem['upperMask'])
                mask = cv2.dilate(mask , self.kernal)
                dontKnowWhyItsExist = cv2.bitwise_and(screenshot, screenshot, mask=mask)
                contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                # print(tmp['contours'])
                result = {"contours": [], "coors": []}
                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if area > elem['minArea']:
                        tmp = {}
                        tmp['x'], tmp['y'], tmp['w'], tmp['h'] = cv2.boundingRect(contour)
                        if self.applyConditions(tmp, elem['conditions']):
                            result['coors'].append(tmp)
                            result['contours'].append(contour)
                self.results[key] = result
                #print(json.dumps(tmp['results'], indent=4))
        #print("\n\n")


    def stop(self):
        super().stop()

    def run(self):
        self.loop_time = time()
        while not self.stopped:
            self.scanDatas()
            # if self.draw:
            # self.drawResult()
            if self.fps:
                if time() - self.loop_time > 0:
                    print('{} fps = {}/s'.format(self.name, 1 / (time() - self.loop_time)))

            sleep(0.01)
            self.loop_time = time()
