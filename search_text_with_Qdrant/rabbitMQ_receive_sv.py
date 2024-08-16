# docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
#!python -m pip install pika --upgrade

import pika
import os
import sys

def main():
    rabbitmq_config = {
    "HostName": "10.0.0.85",
    "UserName": "user",
    "Password": "user",
    "Port": 5672,
    "VirtualHost": "text",
    "QueryQueue": "queue_text_client",
    "ResponseQueue": "queue_text_server"
    }
    # Kết nối đến RabbitMQ
    credentials = pika.PlainCredentials(rabbitmq_config["UserName"], rabbitmq_config["Password"])
    parameters = pika.ConnectionParameters(rabbitmq_config["HostName"], rabbitmq_config["Port"], rabbitmq_config["VirtualHost"], credentials)
    connection = pika.BlockingConnection(parameters)
    # # thiết lập kết nối với máy chủ local
    # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    
    channel = connection.channel()

    # Tạo hàng đợi nếu chưa tồn tại
    channel.queue_declare(queue=rabbitmq_config["ResponseQueue"], durable=True)

    '''
    Kiếm tra danh sách hàng đợi đã tồn tại
    rabbitmqctl.bat list_queues
    '''

    # hàm này sẽ in nội dung của tin nhắn lên màn hình
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        print(" [x] Done")
        #ch.basic_ack(delivery_tag = method.delivery_tag)

    #  cho RabbitMQ biết rằng hàm gọi lại cụ thể này sẽ nhận tin nhắn từ hàng đợi hello
    channel.basic_consume(queue=rabbitmq_config["ResponseQueue"],
                        auto_ack=True, # ?
                        on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
