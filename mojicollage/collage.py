from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from .const import *

def createCollage(inputFileName):
    img = Image.open(settings.MEDIA_ROOT + "/" + inputFileName)
    draw = ImageDraw.Draw(img)

    samplemoji =  "日本語のサンプルMoji♡！！？？!?"

    # 文字
    moji = samplemoji
    # 色
    textRGB = DEEP_PINK
    # サイズ
    textSize = 64
    # フォント
    fnt = ImageFont.truetype(settings.MEDIA_ROOT + "/Font/" + KFHIMAJI, textSize)
    # 座標
    x, y = getMidPointSt(img, draw, samplemoji, fnt)
    
    drawText(draw, x, y, moji, textRGB, fnt, 'black')

    # 保存
    img.save(settings.MEDIA_ROOT + "/" + inputFileName, quality=95)

# 中点
def getMidPoint(img):
    x = img.size[0] / 2
    y = img.size[1] / 2
    return x, y

# 中心に文字が来る時の始点
def getMidPointSt(img, draw, moji, fnt):
    draw_text_width, draw_text_height = draw.textsize(moji, font=fnt)
    x, y = getMidPoint(img)
    x = x - draw_text_width / 2
    y = y - draw_text_height / 2
    return x, y

# 描画
def drawText(draw, x, y, moji, textRGB, fnt, fuchi):
    
    if fuchi != "":
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

