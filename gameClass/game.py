from time import sleep

from util.jsonfunction import jsonPrint
from util.pixel import centerCoor
from util.threadclass import ThreadClass


class Game(ThreadClass):
    HOME = 0
    PVP = 1

    def __init__(self, wc, dpc, action, dataPickData, screenPosition):
        super().__init__()
        self.wc = wc
        self.dpc = dpc
        self.state = self.HOME
        self.action = action
        self.dataPickData = dataPickData
        self.screenPosition = screenPosition
        pass

    def stop(self):
        super().stop()


    def startPvp(self):
        self.lock.acquire()
        self.state = self.PVP
        self.lock.release()

    def run(self):
        while not self.stopped:
            if self.state == self.HOME:
                if self.dpc.hasCoors("lvlUp", "lvl"):
                    CoorslvlUp = self.dpc.getCoors("lvlUp", "lvl")
                    if len(CoorslvlUp) > 0:
                        for coorLvlUp in CoorslvlUp:
                            self.action.do("lvlUpCrew", coorLvlUp)
                            sleep(1)
                        print("DOne")
                        sleep(10)
            elif self.state == self.PVP:
                self.action.goPvp()
            sleep(0.01)
