from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
import chat.rabbitMQ
import json

#定义一个全局rabbitMQMiddleware
rabbitMQMiddleWare = rabbitMQMiddleWare()


#储存消息
#格式：用户名：[{},{},{},{}]-消息
globalMsg = dict()

# Create your views here.
def login(request):
    if (request.method == 'GET'):
        return render(request, 'login.html')
        

def getMsg(request,id):
    if (id in globalMsg.keys()):
        return dict[id]