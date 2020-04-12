from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from chat.rabbitMQ import RabbitMQMiddleWare,RabbitMQReceiver,globalMsg
import json
import threading
import datetime


#定义一个全局rabbitMQMiddleware
rabbitMQMiddleWare = RabbitMQMiddleWare()

# Create your views here.
def login(request):
    #接收登录页面传来的用户id   
    if (request.method == 'GET'):
        return render(request, 'login.html')
    elif request.POST:
        loginId = request.POST.get('loginId',None)
        print(loginId)
        if (not loginId in globalMsg.keys()):
            globalMsg[loginId] = []
            thread = threading.Thread(target=createNewReceiver,args=(loginId,))
            thread.start()
            # receiver = RabbitMQReceiver(loginId)
        return render(request, 'chat.html', {'loginId':loginId})

def sendMsg(request, sendUser, targetUser, msgType, msg):
    """
    发送消息
    """
    if (msgType == 'group'):
        rabbitMQMiddleWare.sendGroupMsg(msg, targetUser, sendUser)
    else:
        rabbitMQMiddleWare.sendSingleMsg(msg, targetUser,sendUser)
    
    if (sendUser in globalMsg.keys()):
        globalMsg[sendUser].append({'sendUser':sendUser, 'msgType':msgType, 'time':datetime.datetime.now().strftime('%H:%M:%S'),'msg':msg})

    return HttpResponse('ok')

def getMsg(request,userID):
    if (userID in globalMsg.keys()):
        return HttpResponse(json.dumps({'res':globalMsg[userID]}))
    return HttpResponse({'res':'null'})

def createNewReceiver(loginId):
    print("boot")
    receiver = RabbitMQReceiver(loginId)

    