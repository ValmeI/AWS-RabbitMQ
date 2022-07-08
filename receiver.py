from basicClient import BasicPikaClient
from file import save_message_to_file
from AWS_S3 import S3Actions
import datetime
import os
# Import RabbitMQ connection variables separately, so they are in one place
from config import rabbitmq_broker_id, rabbitmq_user, rabbitmq_password, rabbitmq_queue_name, aws_region
# Import AWS S3 connection variables separately, so they are in one place
from config import aws_s3_access_key, aws_s3_access_secret, aws_s3_bucket_name
from app_logging import logObject

# get current working directory
working_directory = os.getcwd()


class BasicMessageReceiver(BasicPikaClient):

    # get current message count from, just to show how much msg there was in queue, before starting a consumer
    def get_queue_message_count(self, queue_name, durable):
        logObject.warning(f"Trying to declare queue({queue_name})...")
        queue = self.channel.queue_declare(queue=queue_name, durable=durable)
        msg_cnt = queue.method.message_count
        logObject.warning(f'Before processing - Queue: {queue_name} message count is  {msg_cnt} messages')

    # to get one message at the time. Not using it actually
    def get_message(self, queue):
        method_frame, header_frame, body = self.channel.basic_get(queue)
        if method_frame:
            logObject.warning(method_frame, header_frame, body)
            self.channel.basic_ack(method_frame.delivery_tag)
            return method_frame, header_frame, body
        else:
            logObject.warning('No message returned')

# callable on_message_callback: Required function for dispatching messages
#             to user, having the signature:
#             on_message_callback(channel, method, properties, body)
#              - channel: BlockingChannel
#              - method: spec.Basic.Deliver
#              - properties: spec.BasicProperties
#              - body: bytes
    # listening for messages form given queue and callbacking
    def consume_messages(self, queue):
        def callback(channel, method, properties, body):
            logObject.warning('----------------------------------------------------------------------------')
            logObject.warning(f' [x] Received Message: {body}')
            file_info = save_message_to_file(working_directory, body, True)
            # get saved file full path and filename for S3 upload (next step)
            filename_with_path = file_info[0]
            just_filename = file_info[1]

            # define aws S3 connection
            aws = S3Actions(aws_s3_access_key, aws_s3_access_secret)

            # input: filename_with_path, bucket_name, file_name, upload_folder
            aws.upload_s3_file(filename_with_path, aws_s3_bucket_name, just_filename, str(datetime.date.today()))
            logObject.warning(f'    [x] Message {body} uploaded to AWS S3')
            logObject.warning('----------------------------------------------------------------------------')

        # not sure if auto_ack should be false and then call it manually as
        # auto_ack: if set to True, automatic acknowledgement mode
        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

        logObject.warning(' [*] Waiting for messages')
        self.channel.start_consuming()

    def close(self):
        self.channel.close()
        self.connection.close()


if __name__ == "__main__":

    # Create Basic Message Receiver which creates a connection
    # and channel for consuming messages.
    basic_message_receiver = BasicMessageReceiver(
        rabbitmq_broker_id,
        rabbitmq_user,
        rabbitmq_password,
        aws_region,
    )

    logObject.warning(f'Starting a connection to AWS RabbitMQ')
    logObject.warning(f'Connected to BROKER: {basic_message_receiver.connection}')

    # get message count in queue
    basic_message_receiver.get_queue_message_count(rabbitmq_queue_name, True)

    try:
        # Consume the message that are in queue
        basic_message_receiver.consume_messages(rabbitmq_queue_name)
    except KeyboardInterrupt:
        # When terminating or stopping a script
        logObject.warning('Interrupted')

    # Close connections.
    basic_message_receiver.close()

    logObject.warning(f'Closed BROKER connection: {basic_message_receiver.connection}')

    #TODO: imporeved error handling, connection recovery, concurrency and so on

