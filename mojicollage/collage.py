from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from .const import *
import os
import cv2
import random
import string

def createCollage(inputFileName, imgKey):
    """作成メイン処理：作業用フォルダのファイル名、キー、拡張子"""
    
    face_list = GetFaceXY(inputFileName, imgKey)

    # 顔の取得に失敗した場合、何もしないで終了
    if face_list is None:
        return

    img = Image.open(settings.MEDIA_ROOT + '/' + inputFileName)
    draw = ImageDraw.Draw(img)

    samplemoji =  '日本語のサンプルMoji♡！！？？!?'

    # ----------------------  文字  ----------------------------
    moji = samplemoji
    # ----------------------  色  ------------------------------
    textRGB = DEEP_PINK
    # ----------------------  サイズ  --------------------------
    textSize = 64
    # ----------------------  フォント  ------------------------
    fnt = ImageFont.truetype(settings.MEDIA_ROOT + '/Font/' + KFHIMAJI, textSize)
    # ----------------------  座標  ----------------------------
    x, y = getMidPointSt(img, draw, samplemoji, fnt)
    
    # ----------------------  描画  ----------------------------
    drawText(draw, x, y, moji, textRGB, fnt, 'black')

    # 保存
    img.save(settings.MEDIA_ROOT + '/' + inputFileName, quality=95)


def getMidPoint(img):
    """画像全体の中点"""
    x = img.size[0] / 2
    y = img.size[1] / 2
    return x, y


def getMidPointSt(img, draw, moji, fnt):
    """中心に文字が来る時の始点"""
    draw_text_width, draw_text_height = draw.textsize(moji, font=fnt)
    x, y = getMidPoint(img)
    x = x - draw_text_width / 2
    y = y - draw_text_height / 2
    return x, y


def drawText(draw, x, y, moji, textRGB, fnt, fuchi):
    """描画"""
    if fuchi != '':
        # 文字のふちあり
        draw.text((x, y), 
            moji,
            fill=textRGB,
            font=fnt,
            stroke_width=4,
            stroke_fill=fuchi)
    else:
        # 文字のふちなし
        draw.text((x, y), 
            moji,
            fill=textRGB,
            font=fnt,)


def GetFaceXY(inputFileName, imgKey):
    """顔を検出"""

    #カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(settings.MEDIA_ROOT + '/cascade_file/haarcascade_frontalface_alt.xml')
    imgCv2 = cv2.imread(settings.MEDIA_ROOT + '/' + inputFileName)
    imgCv2_gray = cv2.cvtColor(imgCv2, cv2.COLOR_BGR2GRAY)
    
    # region 物体認識（顔認識）の実行
    #image – CV_8U 型の行列．ここに格納されている画像中から物体が検出されます
    #  →　なぜかグレースケール画像で指定
    #objects – 矩形を要素とするベクトル．それぞれの矩形は，検出した物体を含みます
    #scaleFactor – 各画像スケールにおける縮小量を表します 
    #  →　大きいほど誤検知が多く、小さいほど未検出が多い
    #minNeighbors – 物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む必要があります
    #  →　大きいほど信頼性が上がるが、顔を見逃してしまう率も高くなる。
    #flags – このパラメータは，新しいカスケードでは利用されません．古いカスケードに対しては，cvHaarDetectObjects 関数の場合と同じ意味を持ちます
    #minSize – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
    #  →　これより小さい顔は無視される
    # endregion
    face_list = cascade.detectMultiScale(imgCv2_gray, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))
    
    if len(face_list) == 0:
        return

    #検出した顔を囲む矩形の作成
    for rect in face_list:
        cv2.rectangle(imgCv2, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), (255, 255, 255), thickness=2)
    
    #検出結果の保存(デバッグ用)
    cv2.imwrite(settings.MEDIA_ROOT + '/wk/face_' + imgKey + '.jpg', imgCv2)

    return face_list



def GetRandomStr(num):
    """ランダムな文字列の生成"""
    # 英数字をすべて取得
    dat = string.digits + string.ascii_lowercase + string.ascii_uppercase
    # 英数字からランダムに取得
    return ''.join([random.choice(dat) for i in range(num)])

def SaveTmp(saveFileName, imgKey):
    """作業用フォルダにコピーを作成（ファイル形式を.jpgに統一）"""
    img = Image.open(settings.MEDIA_ROOT + '/' + saveFileName)
    path, ext = os.path.splitext(saveFileName)
    if ext is not None:
        ext = ext.lower()    
    # pngの場合、jpgに変換
    if ext == '.png':
        img = img.convert('RGB')
    
    tmpFileName = 'wk/' + imgKey + '.jpg'
    img.save(settings.MEDIA_ROOT + '/' + tmpFileName, quality=95)
    return tmpFileName
