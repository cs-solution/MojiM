import sys
from .const import *
from PIL import ImageFont
from django.conf import settings
import math
import unicodedata


class ElementInfo:
    """Element（矩形）　親クラス"""
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.width = max.x - min.x
        self.hight = max.y - min.y
        self.size = self.width * self.hight


class ImgInfo(ElementInfo):
    """画像情報"""
    def __init__(self, img):
        super().__init__(
            Point(0, 0),
            Point(img.size[0], img.size[1])
            )
        self.img = img
        """PILのImg"""


class FaceInfo(ElementInfo):
    """顔情報"""
    def __init__(self, rect):
        super().__init__(
            Point(rect[0], rect[1]),
            Point(rect[0]+rect[2], rect[1]+rect[3])
            )
        self.rect = rect
        """情報源"""


class MojiBoxInfo(ElementInfo):
    """文字ボックス情報"""
    def __init__(self, min, max, haichi):
        super().__init__(min, max)
        self.haichi = haichi
        """顔に対する文字の位置（顔の上の余白、顔の右の余白……など）"""
        self.aspScore = 0 
        """アスペクト比に基づくスコア"""
        self.sizeScore = 0
        """面積に基づくスコア"""
        self.moji = ''
        """設定する文字"""
        self.mojiDivision = ''
        """改行ごとに分割された状態の文字"""
        self.mojiRGB = ()
        """文字色RGB"""
        self.fuchi = ''
        """文字のふちの色　：　指定しない場合ふちなし"""
        self.mojiSize = 0
        """文字の大きさ"""
        self.mojiKind = ''
        """文字の種類（書体）"""
        self.IsVertical = False
        """縦書きor横書き　：　縦書きの場合はTrue"""
        self.mojiAlign = ''
        """枠内での文字の位置　：　中央揃え、左揃え……など"""

    def setMojiDivision(self):
        """文字を改行で分割"""
        self.moji = self.moji.replace('\\n', '\n')
        self.mojiDivision = self.moji.splitlines()

    def getMojiSize(self):
        """枠内に収まる最大の文字サイズを求める（余裕を持たせるために0.9倍で少し小さく）"""
        # 立幅に基づく最大の文字サイズ
        hSize = self.hight / len(self.mojiDivision)
        # 横幅に基づく最大の文字サイズ
        wSize = self.width / (self.getMojiMaxWidth() / 2)
        # 小さいほうを採用
        maxSize = hSize if hSize < wSize else wSize
        return math.floor(maxSize * 0.9)

    def setFnt(self):
        """フォントの決定"""
        self.fnt = ImageFont.truetype(
            settings.MEDIA_ROOT + '/Font/' + self.mojiKind, 
            self.mojiSize
            )

    def setMojiAdjustment(self):
        """枠内での文字の調整して再設定"""
        newMojiDivision = []
        maxWidth = self.getMojiMaxWidth()
        if self.mojiAlign == ALIGN_CENTER:
            for x in self.mojiDivision:
                newMojiDivision.append(x.center(maxWidth - (get_east_asian_width_count(x) - len(x))))
            self.mojiDivision = newMojiDivision
        elif self.mojiAlign == ALIGN_RIGHT:
            for x in self.mojiDivision:
                newMojiDivision.append(x.rjust(maxWidth - (get_east_asian_width_count(x) - len(x))))
            self.mojiDivision = newMojiDivision
        self.moji = '\n'.join(self.mojiDivision)

    def getMojiMaxWidth(self):
        """一番文字数が多い行のバイト数"""
        self.setMojiDivision()
        sortedLine = sorted(self.mojiDivision, key=lambda x: get_east_asian_width_count(x), reverse=True)
        return get_east_asian_width_count(sortedLine[0])


class Point:
    """点"""
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

def getEmptySpace(imgInfo, faceArea):
    """上下左右の空きスペースを求める PIL"""
    
    # 上
    uMojiBox = MojiBoxInfo(imgInfo.min, Point(imgInfo.max.x, faceArea.min.y), UP)
    # 下
    dMojiBox = MojiBoxInfo(Point(imgInfo.min.x, faceArea.max.y), imgInfo.max, DOWN)
    # 右
    rMojiBox = MojiBoxInfo(Point(faceArea.max.x, imgInfo.min.y), imgInfo.max, RIGHT)
    # 左
    lMojiBox = MojiBoxInfo(imgInfo.min, Point(faceArea.min.x, imgInfo.max.y), LEFT)

    return [uMojiBox, dMojiBox, rMojiBox, lMojiBox]

def get_east_asian_width_count(text):
    # 文字列のバイト数を返す
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count

def getMidPoint(e):
    """範囲全体の中点を取得 PIL"""
    return Point((e.max.x + e.min.x) / 2, (e.max.y + e.min.y)  / 2)


