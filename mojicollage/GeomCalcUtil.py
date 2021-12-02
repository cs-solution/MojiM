import sys

from cv2 import fastAtan2


class ElementInfo:
    """Element（矩形）　親クラス"""
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.width = max.x - min.x
        self.hight = max.y - min.y
        self.size = self.width * self.hight

class FaceInfo(ElementInfo):
    """顔情報"""
    def __init__(self, rect):
        super().__init__(
            Point(rect[0], rect[1]),
            Point(rect[0]+rect[2], rect[1]+rect[3])
            )
        self.rect = rect

class MojiBoxInfo(ElementInfo):
    """文字ボックス情報"""
    def __init__(self, min, max):
        super().__init__(min, max)
        self.aspScore = 0 
        """アスペクト比に基づくスコア"""
        self.sizeScore = 0
        """面積に基づくスコア"""
        self.moji = ''
        """設定する文字"""
        self.mojiRGB = ()
        """文字色"""
        self.mojiSize = 0
        """文字の大きさ"""
        self.mojiKind = ''
        """文字の種類"""
        self.vertical = False
        """縦書きの場合:True"""
        self.mojiAnchor = ''
        """文字の配置（anchor）"""




class Point:
    """座標"""
    def __init__(self, x, y):
        self.x = x
        self.y = y


# 関数
def unionFaceArea(faceInfoList):
    """顔座標を連結して一つの大きな塊にする"""
    minX = sys.maxsize
    minY = sys.maxsize
    maxX = 0
    maxY = 0
    for info in faceInfoList:
        minX = info.min.x if minX > info.min.x else minX
        minY = info.min.y if minY > info.min.y else minY
        maxX = info.max.x if maxX < info.max.x else maxX
        maxY = info.max.y if maxY < info.max.y else maxY

    return ElementInfo(Point(minX, minY), Point(maxX, maxY))

def getEmptySpace(img, faceArea):
    """上下左右の空きスペースを求める PIL"""

    return


def getMidPoint(img):
    """画像全体の中点 PIL"""
    return Point(img.size[0] / 2, img.size[1] / 2)

def getMidPointSt(img, draw, moji, fnt):
    """中心に文字が来る時の始点 PIL"""
    draw_text_width, draw_text_height = draw.textsize(moji, font=fnt)
    mid = getMidPoint(img)
    x = mid.x - draw_text_width / 2
    y = mid.y - draw_text_height / 2
    return Point(x, y)
