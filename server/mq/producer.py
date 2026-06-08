import json
import pika

def publish_message(data):

    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost")
    )

    channel = connection.channel()

    channel.queue_declare(
        queue="clinica_queue",
        durable=True
    )

    channel.basic_publish(
        exchange="",
        routing_key="clinica_queue",
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    connection.close()
