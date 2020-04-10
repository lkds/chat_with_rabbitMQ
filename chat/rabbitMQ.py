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
            pika.ConnectionParameters(hostAddress, credentials=credentials))

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='topic_chat', exchange_type='topic')
    
    def sendSingleMsg(self,msg, id):
        """
        发送单聊消息
        """
        self.channel.basic_publish(
            exchange='topic_chat', routing_key='message.single.' + id, body=msg)

    def sendGroupMsg(self,msg, groupID=''):
        """
        发送群聊消息
        """
        self.channel.basic_publish(
            exchange='topic_chat', routing_key='message.group', body=msg)
    
    def closeConnection(self):
        self.connection.close()


class RabbitMQReceiver:
    def __init__(self, id):
        self.id = id
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(hostAddress, credentials=credentials))

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='topic_chat', exchange_type='topic')
        result = self.channel.queue_declare('', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(
            exchange='topic_chat', queue=self.queue_name, routing_key='message.*.'+id)
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.on_response, auto_ack=True)
        self.channel.start_consuming()
    
    def on_response(self, ch, method, props, body):
        msgInfo = method.routing_key.split('.')[2]
        sendUser = msgInfo[2]
        msgType = msgInfo[1]
        globalMsg[id].append({'sendUser':sendUser, 'msgType':msgType, 'time':datetime.datetime.now().strftime('%H:%M:%S'),'msg':body})