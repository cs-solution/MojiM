from django.conf import settings
from PIL import Image, ImageDraw
from .const import *
from .GeomCalcUtil import *
from .DBUtil import *
import cv2
import random


def createCollage(inputFileName, imgKey):
    """作成メイン処理：作業用フォルダのファイル名、キー"""
    
    # ----------------------  顔情報取得  ------------------------------
    faceInfoList = getFaceInfo(inputFileName, imgKey)
    if faceInfoList is None:
        # 顔の取得に失敗した場合、何もしないで終了
        return

    # 画像を開く
    img = Image.open(settings.MEDIA_ROOT + '/' + inputFileName)
    imgInfo = ImgInfo(img)

    # ----------------------  領域計算  --------------------------------
    faceArea = unionFaceArea(faceInfoList)
    mojiBoxList = getEmptySpace(imgInfo, faceArea)

    # ----------------------  スコア計算  ------------------------------
    mojiBoxList = getAspScore(mojiBoxList)
    mojiBoxList = getSizeScore(imgInfo, mojiBoxList)
    
    mojiBoxList = sorted(mojiBoxList, key=lambda x: x.aspScore + x.sizeScore, reverse=True)

    mojiBox1 = mojiBoxList[0]
    # ----------------------  設定する文字  ----------------------------
    con = connect()
    res = getData(con, 'SELECT * FROM serif ORDER BY random() LIMIT 1;')
    if res is None or len(res) == 0:
        # 文字の取得に失敗した場合、何もしないで終了
        return
    mojiBox1.moji = res[0][1]
    mojiBox1.setMojiDivision()
    # ----------------------  文字色  ----------------------------------
    mojiBox1.mojiRGB = PINK
    # ----------------------  文字ふちの色  ----------------------------
    mojiBox1.fuchi = 'black'
    # ----------------------  文字の種類  ------------------------------
    mojiBox1.mojiKind = HGRPP1
    # ----------------------  縦書きor横書き  --------------------------
    mojiBox1.IsVertical = False
    # ----------------------  文字の大きさ  ----------------------------
    mojiBox1.mojiSize = mojiBox1.getMojiSize()
    # ----------------------  フォント  --------------------------------
    mojiBox1.setFnt()
    # ----------------------  枠内での文字の位置  ----------------------
    mojiBox1.mojiAlign = ALIGN_CENTER
    mojiBox1.setMojiAdjustment()
    # ----------------------  座標  ------------------------------------
    midPt = getMidPoint(mojiBox1)    
    # ----------------------  フィルタ  --------------------------------
    fNo = random.randint(1, 5)
    setFilter(imgInfo, fNo, 90)
    # ----------------------  描画  ------------------------------------
    draw = ImageDraw.Draw(imgInfo.img)
    drawText(draw, midPt, mojiBox1)

    # 保存
    imgInfo.img.save(settings.MEDIA_ROOT + '/' + inputFileName, quality=95)


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
    
    if len(face_list) == 0:
        return

    # FaceInfo作成
    faceInfoList = []
    for rect in face_list:
        faceInfoList.append(FaceInfo(rect))

    # 検出した顔を囲む矩形の作成(デバッグ用)
    for rect in face_list:
        cv2.rectangle(imgCv2, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (255, 255, 255), thickness=2)
    cv2.imwrite(settings.MEDIA_ROOT + '/wk/face_' + imgKey + '.jpg', imgCv2)

    return faceInfoList

def getAspScore(mojiBoxList):
    """アスペクト比に基づくスコア：アスペクト比が正方形に近いほど高得点"""
    for box in mojiBoxList:
        asp = box.width / box.hight if box.width > box.hight else box.hight / box.width
        if asp < 1.2:
            box.aspScore = 6
        elif asp < 1.5:
            box.aspScore = 5
        elif asp < 2:
            box.aspScore = 3
        elif asp < 3:
            box.aspScore = 2
        elif asp < 4:
            box.aspScore = 1
        else:
            box.aspScore = 0

    return mojiBoxList

def getSizeScore(imgInfo, mojiBoxList):
    """面積に基づくスコア：面積が大きいほど高得点"""
    for box in mojiBoxList:
        pct = box.size / imgInfo.size
        if pct > 0.7:
            box.sizeScore = 3
        elif pct > 0.5:
            box.sizeScore = 2
        elif pct > 0.2:
            box.sizeScore = 1
        else:
            box.sizeScore = 0

    return mojiBoxList

def setFilter(imgInfo, fNo, depth):
    """フィルタセット"""
    fil = None
    if fNo == 1:
        fil = Image.open(settings.MEDIA_ROOT + '/Filter/' + 'f1.png')
    elif fNo == 2:
        fil = Image.open(settings.MEDIA_ROOT + '/Filter/' + 'f2.png')
    elif fNo == 3:
        fil = Image.open(settings.MEDIA_ROOT + '/Filter/' + 'f3.png')
    elif fNo == 4:
        fil = Image.open(settings.MEDIA_ROOT + '/Filter/' + 'f4.png')
    if fil is None:
        return
    fil = fil.crop((imgInfo.min.x, imgInfo.min.y, imgInfo.max.x, imgInfo.max.y))
    fil.putalpha(depth)
    imgInfo.img = Image.alpha_composite(imgInfo.img, fil)

def drawText(draw, pt, mojiBoxInfo):
    """描画"""
    if mojiBoxInfo.fuchi != '':
        # 文字のふちあり
        draw.multiline_text((pt.x, pt.y), 
            mojiBoxInfo.moji,
            fill=mojiBoxInfo.mojiRGB,
            font=mojiBoxInfo.fnt,
            anchor='mm',
            spacing=0,
            stroke_width=4,
            stroke_fill=mojiBoxInfo.fuchi,
            )
    else:
        # 文字のふちなし
        draw.multiline_text((pt.x, pt.y), 
            mojiBoxInfo.moji,
            fill=mojiBoxInfo.mojiRGB,
            font=mojiBoxInfo.fnt,
            anchor='mm',
            spacing=0,
            )
