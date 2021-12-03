from django.conf import settings
from PIL import Image
import random
import string
import os


def createKey(num):
    """ランダムな文字列の生成"""
    # 英数字をすべて取得
    dat = string.digits + string.ascii_lowercase + string.ascii_uppercase
    # 英数字からランダムに取得
    return ''.join([random.choice(dat) for i in range(num)])

def saveTmp(saveFileName, imgKey):
    """作業用フォルダにコピーを作成（ファイル形式を.jpgに統一し、大きすぎる場合はリサイズ）"""
    img = Image.open(settings.MEDIA_ROOT + '/' + saveFileName)
    path, ext = os.path.splitext(saveFileName)
    if ext is not None:
        ext = ext.lower()    
    # jpgの場合、pngに変換
    if ext == '.jpg' or ext == '.jpeg':
        img = img.convert('RGBA')
    # 大きすぎる画像はリサイズ
    if img.width > 2000 or img.height > 2000:
        if img.height > img.width:
            img = scale_to_height(img, 2000)
        else:
            img = scale_to_width(img, 2000)

    tmpFileName = 'wk/' + imgKey + '.png'
    img.save(settings.MEDIA_ROOT + '/' + tmpFileName, quality=95)
    return tmpFileName
 
def scale_to_height(img, height):
    """アスペクト比を固定して、高さが指定した値になるようリサイズする。"""
    width = round(img.width * height / img.height)
    return img.resize((width, height))

def scale_to_width(img, width):
    """アスペクト比を固定して、幅が指定した値になるようリサイズする。"""
    height = round(img.height * width / img.width)
    return img.resize((width, height))