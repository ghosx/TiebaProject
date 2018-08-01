from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import utils
from .models import Tieba,User


# Create your views here.
stoken = 'e7f5d88e4f9128fe12a5b0d76f9ec21c59a006e1b720bf4dd83c14dd645ad5c1'


def index(request):
    if request.method == "GET":
        return render(request,'index.html')
    elif request.method == "POST":
        bduss = request.POST.get('bduss','default')
        if len(bduss) != 192:
            return HttpResponse('BDUSS WRONG')
        else:
            name = utils.getUsernameByBduss(bduss)
            user = User(bduss=bduss, username=name, idDel=False)
            user.save()
            tb = utils.getFavorite(bduss,stoken)
            for i in tb:
                Tb = Tieba(name=i[0],fid=i[1],tbjingyan=i[2],tbdengji=i[3])
                Tb.save()
                Tb.user.add(user)
            return HttpResponse(str(len(tb))+'updateok!')