# docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
#!python -m pip install pika --upgrade
import pika
import json

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
channel.queue_declare(queue=rabbitmq_config["QueryQueue"], durable=True)

# -> sẵn sàng gửi tin nhắn
body = 'Điều 2. Sở Lao động - Thương binh và Xã hội căn cứ danh mục vị trí việc làm; số lượng người làm việc và lao động hợp đồng; cơ cấu chức danh nghề nghiệp; bản mô tả vị trí việc làm, khung năng lực của từng vị trí việc làm trong Đề án kèm theo Quyết định này để làm cơ sở thực hiện tuyển dụng, sử dụng, đào tạo, bồi dưỡng, quản lý số lượng người làm việc và lao động hợp đồng theo quy định của pháp luật, đảm bảo hoàn thành tốt nhiệm vụ được giao.'

channel.basic_publish(exchange='',
                      routing_key=rabbitmq_config["QueryQueue"],  # tên hàng đợi
                      body=body.encode('utf-8'))
print(f" [x] Sent {body}'")

# đóng kết nối:
connection.close()
