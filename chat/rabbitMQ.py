import pika
import datetime

#储存消息
#格式：用户名：[{},{},{},{}]-消息
globalMsg = dict()

"""
{
    用户名1:[
        {sendUser:'', type:'', time：'xxx',msg:'xxx'},
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
        {发送方显示}
    ],
    paidaye:[
        {time:'10:34',msg:'hi'},
        {time:'10:35',msg:'nihao'},
        {time:'10:36',msg:'zaijian'},
        {time:'10:38',msg:'hehh'},
        {time:'10:39',msg:'xxx'}
        {}
    ],
}
"""

hostAddress = '47.113.123.159'
credentials = pika.PlainCredentials('fnzs', '1369842')
class RabbitMQMiddleWare:
    """
    负责消息的发送
    全局一个
    """
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(hostAddress, credentials=credentials,heartbeat=0))

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='topic_chat', exchange_type='topic')
    
    def sendSingleMsg(self,msg, userID, sendUser):
        """
        发送单聊消息
        """
        self.channel.basic_publish(
            exchange='topic_chat', routing_key='message.single.' + userID + '.' + sendUser, body=msg)

        print( sendUser+'向'+userID+'单发'+msg)
        globalMsg[sendUser].append({'sendUser': sendUser,'recvUser':userID, 'msgType':'single', 'time': datetime.datetime.now().strftime('%H:%M:%S'), 'msg': msg})


    def sendGroupMsg(self,msg, sendUser):
        """
        发送群聊消息
        """
        self.channel.basic_publish(
            exchange='topic_chat', routing_key='message.group.'+ sendUser, body=msg)
        print(sendUser+'群发'+msg)
        globalMsg[sendUser].append({'sendUser': sendUser,'recvUser':'祖安交流', 'msgType':'group', 'time': datetime.datetime.now().strftime('%H:%M:%S'), 'msg': msg})
    
    def paidaye(self):
        self.channel.basic_publish(exchange='topic_chat', routing_key='paidaye.yellow.dog', body="ping")

    def sendLoginInfo(self, userID):
        self.channel.basic_publish(
            exchange='topic_chat', routing_key='sys.login.'+ userID, body='null')

    def closeConnection(self):
        self.connection.close()


class RabbitMQReceiver:
    def __init__(self, userID):
        self.userID = userID
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(hostAddress, credentials=credentials,heartbeat=0))

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='topic_chat', exchange_type='topic')
        result = self.channel.queue_declare('', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(
            exchange='topic_chat', queue=self.queue_name, routing_key='message.single.' + self.userID + '.*')
        self.channel.queue_bind(
            exchange='topic_chat', queue=self.queue_name, routing_key='message.group.*')
        self.channel.queue_bind(
            exchange='topic_chat', queue=self.queue_name, routing_key='sys.login.*')
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.on_response, auto_ack=True)
        self.channel.start_consuming()
    
    def on_response(self, ch, method, props, body):
        msgInfo = method.routing_key.split('.')
        mType = msgInfo[0]
        if(mType == "message"):
            msgType = msgInfo[1]
            if(msgType == 'group'):
                sendUser = msgInfo[2]
                print('接收到群发消息')
            else:
                sendUser = msgInfo[3]
            print(sendUser,body)
            if(self.userID ==  sendUser):
                pass           
            else:
                globalMsg[self.userID].append({'sendUser': sendUser,'recvUser':self.userID, 'msgType': msgType, 'time': datetime.datetime.now().strftime('%H:%M:%S'), 'msg': str(body, 'utf8')})
            
        elif (mType == "sys"):
            if(not msgInfo[2] in globalMsg.keys()):
                globalMsg[msgInfo[2]]=[]
