import pika

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
    
    def sendSingleMsg(msg, id):
        """
        发送单聊消息
        """
        self.channel.basic_publish(
            exchange='topic_chat', routing_key='message.single.' + id, body=msg)

    def sendGroupMsg(msg, groupID=''):
        """
        发送群聊消息
        """
        self.channel.basic_publish(
            exchange='topic_chat', routing_key='message.group', body=msg)
    
    def closeConnection():
        self.connection.close()


class RabbitMQReceiver:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(hostAddress, credentials=credentials))

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='topic_chat', exchange_type='topic')
        result = channel.queue_declare('', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=True)
    
    def on_response(self, ch, method, props, body):
        self.receive_user = method.routing_key
        self.receive_body = body

    def receiveSingleChat():
        self.channel.start_consuming()