from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from chat.rabbitMQ import RabbitMQMiddleWare,RabbitMQReceiver
import json

#定义一个全局rabbitMQMiddleware
rabbitMQMiddleWare = RabbitMQMiddleWare()


#储存消息
#格式：用户名：[{},{},{},{}]-消息
globalMsg = dict()


# Create your views here.
def login(request):
    #接收登录页面传来的用户id   
    if (request.method == 'GET'):
        return render(request, 'login.html')
    elif request.POST:
        loginId = request.POST.get('loginId',None)
        print(loginId)
        return render(request, 'login.html', {'loginId':loginId})

def getMsg(request,id):
    if (id in globalMsg.keys()):
        return dict[id]