from django.shortcuts import render
from .forms import createInfo
from django.core.files.storage import default_storage
from .collage import createCollage, GetRandomStr, SaveTmp

# Create your views here.

def home(request):
    """ホーム画面"""
    initial_dict = {
        'tgtSeikaku':'3',
        'tgtKeigo':'0',
        'finish':'1',
    }
    form = createInfo(initial=initial_dict)
    return render(request, 'mojicollage/home.html', {'form': form})

def result(request):
    """結果画面"""
    form = createInfo(request.POST, request.FILES)
    if form.is_valid() and form.errors.__len__()==0:
        img = form.files['tgtImg']
        # キー発行
        imgKey = GetRandomStr(10)
        # 保存用フォルダに保存（キー＋'_'＋原本ファイル名）
        saveFileName = default_storage.save(imgKey+'_' + img.name, img)
        # 作業用フォルダにコピーを作成
        tmpFileName = SaveTmp(saveFileName, imgKey)
        
        createCollage(tmpFileName, imgKey)

        tmpImgUrl = default_storage.url(tmpFileName)
        return render(request, 'mojicollage/result.html', {'imgUrl': tmpImgUrl})
    return render(request, 'mojicollage/home.html', {'form': form})
