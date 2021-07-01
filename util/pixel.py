import cv2
import numpy as np


def centerCoor(data, diff=None):
    if diff is None:
        negCoor = {"x": 0, "y": 0}
    print(data)
    x, y, w, h = (v for v in data.values())
    x = int(x + w / 2) + diff["x"]
    y = int(y + h / 2) + diff["y"]
    print(x, y)
    return {"x": x if x > 0 else 0, "y": y if y > 0 else 0}


def comparePixel(screenShot, coor, color, tolerance=20):
    if screenShot is not None:
        pixel = screenShot[coor['y'], coor['x']]
        # print("{} vs {}".format(pixel, color))
        if abs(pixel[0] - color[0]) <= tolerance:
            if abs(pixel[1] - color[1]) <= tolerance:
                if abs(pixel[2] - color[2]) <= tolerance:
                    return True
    return False


def applyThresh(srcImg):
    img = cv2.cvtColor(srcImg, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (0, 0), fx=2, fy=2)
    kernel = np.ones((2, 2), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    (thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    return img


def getImgRectangle(img, coor):
    cropped = img[coor['y']:coor['y'] + coor['height'], coor['x']:coor['x'] + coor['width']]
    return cropped
