import json, os, django
import pika

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "admin.settings"
)  # use products outside of django
django.setup()

from products.models import Product

params = pika.URLParameters(
    "amqps://lbbaujsq:WVsmzDk445y1xSQBXatb68UycgcROE_i@woodpecker.rmq.cloudamqp.com/lbbaujsq"
)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue="admin")


def callback(ch, method, properties, body):
    print("Received in admin")
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print("Product likes increases!")


channel.basic_consume(queue="admin", on_message_callback=callback, auto_ack=True)

print("Started Consuming")

channel.start_consuming()

channel.close()
