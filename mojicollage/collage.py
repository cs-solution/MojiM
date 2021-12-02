from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from .const import *
from .GeomCalcUtil import *
import cv2

def createCollage(inputFileName, imgKey):
    """作成メイン処理：作業用フォルダのファイル名、キー"""
    
    # 顔情報取得
    faceInfoList = getFaceInfo(inputFileName, imgKey)

    # 顔の取得に失敗したor顔が多すぎる場合、何もしないで終了
    if faceInfoList is None:
        return

    # 画像を開く
    img = Image.open(settings.MEDIA_ROOT + '/' + inputFileName)
    draw = ImageDraw.Draw(img)


    faceArea = unionFaceArea(faceInfoList)
    getEmptySpace(img, faceArea)

    # ----------------------  スコア計算  ------------------------------
    # アスペクト比に基づくスコア計算
    # 面積に基づくスコア計算



    # ----------------------  設定する文字  ----------------------------
    moji = '日本語のサンプルMoji♡！！？？!?'
    # ----------------------  文字色  ----------------------------------
    mojiRGB = DEEP_PINK
    # ----------------------  文字の大きさ  ----------------------------
    mojiSize = 64
    # ----------------------  文字の種類  ------------------------------
    mojiKind = KFHIMAJI
    # ----------------------  フォント  --------------------------------
    fnt = getFnt(mojiKind, mojiSize)
    # ----------------------  座標  ------------------------------------
    midSt = getMidPointSt(img, draw, moji, fnt)
    
    # ----------------------  描画  ----------------------------
    drawText(draw, midSt.x, midSt.y, moji, mojiRGB, fnt, 'black')

    # 保存
    img.save(settings.MEDIA_ROOT + '/' + inputFileName, quality=95)

def drawText(draw, x, y, moji, mojiRGB, fnt, fuchi):
    """描画"""
    if fuchi != '':
        # 文字のふちあり
        draw.text((x, y), 
            moji,
            fill=mojiRGB,
            font=fnt,
            stroke_width=4,
            stroke_fill=fuchi)
    else:
        # 文字のふちなし
        draw.text((x, y), 
            moji,
            fill=mojiRGB,
            font=fnt,)


def getFaceInfo(inputFileName, imgKey):
    """顔を検出"""

    #カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(settings.MEDIA_ROOT + '/cascade_file/haarcascade_frontalface_alt.xml')
    imgCv2 = cv2.imread(settings.MEDIA_ROOT + '/' + inputFileName)
    imgCv2_gray = cv2.cvtColor(imgCv2, cv2.COLOR_BGR2GRAY)
    
    # region 物体認識（顔認識）の実行
    # ↓↓↓↓↓引数↓↓↓↓↓
    # image – CV_8U 型の行列．ここに格納されている画像中から物体が検出されます
    #  →　処理を高速にするためグレースケール画像で指定
    # objects – 矩形を要素とするベクトル．それぞれの矩形は，検出した物体を含みます
    # scaleFactor – 各画像スケールにおける縮小量を表します 
    #  →　大きいほど誤検知が多く、小さいほど未検出が多い
    # minNeighbors – 物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む必要があります
    #  →　大きいほど信頼性が上がるが、顔を見逃してしまう率も高くなる。
    # flags – このパラメータは，新しいカスケードでは利用されません．古いカスケードに対しては，cvHaarDetectObjects 関数の場合と同じ意味を持ちます
    # minSize – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
    #  →　これより小さい顔は無視される
    # ↓↓↓↓↓戻り値↓↓↓↓↓
    # face_list = [0:左上のx座標; 1:左上のy座標; 2:横幅; 3:縦;]のリスト
    # endregion
    face_list = cascade.detectMultiScale(imgCv2_gray, scaleFactor=1.1, minNeighbors=2, minSize=(80, 80))
    
    if len(face_list) == 0 or len(face_list) > 3:
        return

    # FaceInfo作成
    faceInfoList = []
    for rect in face_list:
        faceInfo=FaceInfo(rect)
        faceInfoList.append(faceInfo)

    # 検出した顔を囲む矩形の作成(デバッグ用)
    for rect in face_list:
        cv2.rectangle(imgCv2, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (255, 255, 255), thickness=2)
    cv2.imwrite(settings.MEDIA_ROOT + '/wk/face_' + imgKey + '.jpg', imgCv2)

    return faceInfoList

def getFnt(mojiKind, mojiSize):
    return ImageFont.truetype(settings.MEDIA_ROOT + '/Font/' + mojiKind, mojiSize)