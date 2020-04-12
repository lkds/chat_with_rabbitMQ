from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from chat.rabbitMQ import RabbitMQMiddleWare,RabbitMQReceiver,globalMsg
import json
import threading
import datetime
import pika


#定义一个全局rabbitMQMiddleware
rabbitMQMiddleWare = RabbitMQMiddleWare()


#储存消息
#格式：用户名：[{},{},{},{}]-消息
# globalMsg = dict()

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
        return render(request, 'login.html',{'msg':''})
    elif request.POST:
        loginId = request.POST.get('loginId',None)
        print(loginId)
        if (not loginId in globalMsg.keys()):
            globalMsg[loginId]=[]
            rabbitMQMiddleWare.sendLoginInfo(loginId)
            thread = threading.Thread(target=createNewReceiver, args=(loginId,))
            thread.start()

            # receiver = RabbitMQReceiver(loginId)
        return render(request, 'chat.html', {'loginId': loginId})
        # else:
        #     return render(request, 'login.html', {'msg': '这个昵称太抢手了，换一个吧！'})

def send(sendUser, targetUser, msgType, msg):
    if (msgType == 'group'):
        rabbitMQMiddleWare.sendGroupMsg(msg, sendUser)
    else:
        rabbitMQMiddleWare.sendSingleMsg(msg, targetUser,sendUser)
        
        # if (sendUser in globalMsg.keys()):
        #     globalMsg[sendUser].append({'sendUser':sendUser, 'msgType':msgType, 'time':datetime.datetime.now().strftime('%H:%M:%S'),'msg':msg})

    return HttpResponse('ok')

def sendMsg(request, sendUser, targetUser, msgType, msg):
    """
    发送消息
    """
    if request.method == 'POST':
        if request.POST:
            msgBody = request.POST.get('msgBody','')
            return send(sendUser, targetUser, msgType, msgBody)
    else:
        return send(sendUser, targetUser, msgType, msg)

def getMsg(request,userID):
    if (userID in globalMsg.keys()):
        return HttpResponse(json.dumps({'res':globalMsg[userID]}))
    return HttpResponse({'res':'null'})

def createNewReceiver(loginId):
    print("boot")
    receiver = RabbitMQReceiver(loginId)

def getUserList(request):
    return HttpResponse(json.dumps({'res':list(globalMsg.keys())}))

