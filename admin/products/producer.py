import json
import pika

params = pika.URLParameters(
    "amqps://lbbaujsq:WVsmzDk445y1xSQBXatb68UycgcROE_i@woodpecker.rmq.cloudamqp.com/lbbaujsq"
)

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="", routing_key="main", body=json.dumps(body), properties=properties
    )
