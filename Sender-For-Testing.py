from basicClient import BasicPikaClient
import string
import random

# Import RabbitMQ connection variables separately, so they are in one place
from config import rabbitmq_broker_id, rabbitmq_user, rabbitmq_password, rabbitmq_queue_name, aws_region

'# Made for testing, as its easier that way to greate x amount of messages'


class BasicMessageSender(BasicPikaClient):

    # added Durability input as default is True on RabbitMQ UI when making a new queue manually
    # creates a new or checks given queue
    def declare_queue(self, queue_name, durable):
        print(f"Trying to declare queue({queue_name})...")
        self.channel.queue_declare(queue=queue_name, durable=durable)

    # send a message to given queue
    def send_message(self, exchange, routing_key, body):
        channel = self.connection.channel()
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=body)
        print(f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}, Body: {body}")

    # closes the channel and connection
    def close(self):
        self.channel.close()
        self.connection.close()


if __name__ == "__main__":

    # Initialize Basic Message Sender which creates a connection
    # and channel for sending messages.
    basic_message_sender = BasicMessageSender(
        rabbitmq_broker_id,
        rabbitmq_user,
        rabbitmq_password,
        aws_region,
    )

    # Declare a queue
    basic_message_sender.declare_queue(rabbitmq_queue_name, True)

    # create x amount of message to queue for TESTING
    x = 1
    for nr in range(0, x):
        # add random str of len 10 to body
        random_str = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        str_body = f'TESTING message HELLO-{str(nr)} - {random_str}'
        # Send a message to the queue.
        basic_message_sender.send_message(exchange="",
                                          routing_key=rabbitmq_queue_name,
                                          body=str.encode(str_body))

    # Close connections.
    basic_message_sender.close()
