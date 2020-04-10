from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
import chat.rabbitMQ

def gotoLogin(request):
    return render(request,'login.html')


# Create your views here.
def login(request):
    #接收登录页面传来的用户id   
    if (request.method == 'GET'):
        return render(request,'login.html')
    elif request.POST:
        loginId = request.POST.get('loginId',None)
        print(loginId)
        return render(request, 'login.html',{'msg':'asd'})


