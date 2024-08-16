# docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
#!python -m pip install pika --upgrade
# some_file.py
import sys
import pika
import os
import sys
import json

# caution: path[0] is reserved for script path (or '' in REPL)
# sys.path.insert(1, 'D:\\NLP\\Semantic-Search-in-Vietnam-Legislation\\search_with_text\\search_text_with_Qdrant')
from text_search import searching_text_to_doc #(text_query, my_collection, limit)
# sys.path.insert(1, 'D:\\NLP\\Semantic-Search-in-Vietnam-Legislation\\search_with_text\\search_text_with_Qdrant')
from model_embedding import model_embedding

tokenizer, model = model_embedding()

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
channel = connection.channel()

# Tạo hàng đợi nếu chưa tồn tại
channel.queue_declare(queue=rabbitmq_config["QueryQueue"], durable=True)
channel.queue_declare(queue=rabbitmq_config["ResponseQueue"], durable=True)

# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
# # Tạo hàng đợi, nơi tin nhắn đc gửi đến
# channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    global tokenizer, model
    text = body.decode('utf-8')  # Chuyển đổi từ bytes sang str
    print(f" [x] Received {text}")
    result = searching_text_to_doc(text, my_collection= "Chunking_text_VBPL", limit=20, tokenizer= tokenizer, model = model)
    response = json.dumps(result)
    response = response.encode('utf-8')
    print(f" [x] Send {response}")


    # Gửi kết quả lại hàng đợi
    channel.basic_publish(exchange='',
                          routing_key=rabbitmq_config["ResponseQueue"],
                          body=response)

try:
    channel.basic_consume(queue=rabbitmq_config["QueryQueue"], on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)