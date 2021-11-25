from django.shortcuts import render
from .forms import createInfo

# Create your views here.

def home(request):
    if request.method == "POST":
        form = createInfo(request.POST, request.FILES)
        return render(request, 'mojicollage/home.html', {'form': form})
    else:
        initial_dict = {
            'tgtSeikaku':'3',
            'tgtKeigo':'0',
            'finish':'0',
        }
        form = createInfo(request.POST or None, initial=initial_dict)
        return render(request, 'mojicollage/home.html', {'form': form})

