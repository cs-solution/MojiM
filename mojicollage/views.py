from django.shortcuts import render
from .forms import createInfo

# Create your views here.

def home(request):
    initial_dict = {
        'tgtSeikaku':'3',
        'tgtKeigo':'0',
        'finish':'0',
    }
    form = createInfo(request.POST or None, initial=initial_dict)
    return render(request, 'mojicollage/home.html', {'form': form})

