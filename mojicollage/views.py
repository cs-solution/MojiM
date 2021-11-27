from django.shortcuts import render
from .forms import createInfo
from django.core.files.storage import default_storage
from django.conf import settings
import os

# Create your views here.

def home(request):
    initial_dict = {
        'tgtSeikaku':'3',
        'tgtKeigo':'0',
        'finish':'1',
    }
    form = createInfo(initial=initial_dict)
    return render(request, 'mojicollage/home.html', {'form': form})

def result(request):
    form = createInfo(request.POST, request.FILES)
    if form.is_valid() and form.errors.__len__()==0:
        img = form.files['tgtImg']
        tmpFolderName = "wk/"
        tmpFileName = default_storage.save(tmpFolderName+img.name, img)
        
        tmpImgUrl = default_storage.url(tmpFileName)
        return render(request, 'mojicollage/result.html', {'imgUrl': tmpImgUrl})
    return render(request, 'mojicollage/home.html', {'form': form})
        
