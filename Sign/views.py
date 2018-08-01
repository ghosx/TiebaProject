from django.shortcuts import render
from django.shortcuts import HttpResponse
import json

# Create your views here.

def index(request):
    if request.method == "GET":
        return render(request,'index.html')
    elif request.method == "POST":
        return HttpResponse('aa')
