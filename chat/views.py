from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from chat.rabbitMQ import RabbitMQMiddleWare,RabbitMQReceiver
import json
<<<<<<< HEAD
=======
import threading
import datetime

>>>>>>> 91288f05e8df650c13c6d8b1217e16d2786b28cb

#定义一个全局rabbitMQMiddleware
rabbitMQMiddleWare = RabbitMQMiddleWare()


#储存消息
#格式：用户名：[{},{},{},{}]-消息
globalMsg = dict()

"""
{
    用户名1:[
        {time：'xxx',msg:'xxx'},
        {time：'xxx',msg:'xxx'},
        {time：'xxx',msg:'xxx'},
        ...
    ],
    用户名2:[
        {time：'xxx',msg:'xxx'},
        {time：'xxx',msg:'xxx'},
        {time：'xxx',msg:'xxx'},
        ...
    ]
}

eg:
{
    pilot:[
        {time:'10:34',msg:'hi'},
        {time:'10:35',msg:'nihao'},
        {time:'10:36',msg:'zaijian'},
        {time:'10:38',msg:'hehh'},
        {time:'10:39',msg:'xxx'}
    ],
    paidaye:[
        {time:'10:34',msg:'hi'},
        {time:'10:35',msg:'nihao'},
        {time:'10:36',msg:'zaijian'},
        {time:'10:38',msg:'hehh'},
        {time:'10:39',msg:'xxx'}
    ],
}
"""

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
        rabbitMQMiddleWare.sendGroupMsg(msg)
    else:
        rabbitMQMiddleWare.sendSingleMsg(msg, targetUser)
    
    if (targetUser in globalMsg.keys()):
        globalMsg[targetUser].append({'sendUser':sendUser, 'msgType':msgType, 'time':datetime.datetime.now().strftime('%H:%M:%S'),'msg':msg})

def getMsg(request,id):
    if (id in globalMsg.keys()):
        return HttpResponse(json.dumps({'res':globalMsg[id]}))
    return HttpResponse({'res':'null'})

def createNewReceiver(loginId):
    receiver = RabbitMQReceiver(loginId)

    
