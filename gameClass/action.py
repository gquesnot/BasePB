from time import sleep, time

from util.pixel import centerCoor
from util.threadclass import ThreadClass
import pyautogui


class Action(ThreadClass):
    creewNegCoor = {"x": 15, "y": - 30}

    def __init__(self, offset, center, info, duration=0.1):
        super().__init__()
        self.offsetX = offset[0]
        self.offsetY = offset[1]
        self.center = center
        self.info = info
        self.duration = duration

    def stop(self):
        self.stopped = True

    def goPvp(self):
        print("GOING PVP 3s")
        sleep(3)
        self.moveClick(self.info['galaxy'])
        print("done")
        sleep(5)
        self.moveClick(self.info['pvp'])
        sleep(1)


    def lvlUpCrew(self, coor):
        print("lvlUp in 2s")
        sleep(2)
        self.moveClick(centerCoor(coor, diff=self.info['crewClick']))
        sleep(0.5)
        self.moveClick(centerCoor(coor, diff=self.info['crewLvlUp1']))
        sleep(0.5)
        self.moveClick(self.info['crewLvlUp2'])
        sleep(0.5)
        pyautogui.scroll(-15)
        #self.moveClick(self.info['crewCloseLvlUp2'])

    def centerMouse(self):
        self.moveTo(self.center)

    def moveTo(self, coor):
        pyautogui.moveTo(self.offsetX + coor['x'], self.offsetY + coor['y'], duration=self.duration)

    def click(self):
        pyautogui.mouseDown()
        sleep(self.duration)
        pyautogui.mouseUp()

    def moveClick(self, coor):
        self.moveTo(coor)
        self.click()

    def do(self, action, data):
        t = time()
        if action == "move":
            self.moveTo(data)
        elif action == "moveClick":
            self.moveClick(data)
        elif action == "click":
            self.click()
        elif action == "lvlUpCrew":
            self.lvlUpCrew(data)
        # self.centerMouse()
        print(action + " {}s".format(round(time() - t, 3)))
