import configparser
from app_logging import logObject

# parses config.ini file that is in same directory
configParser = configparser.RawConfigParser()
configFilePath = r'..\AWS-RabbitMQ\config.ini'
parser = configparser.ConfigParser()

# try to open config file
try:
    parser.read(configFilePath)
except Exception as e:
    logObject.warning(e)

# RabbitMQ
rabbitmq_broker_id = parser.get('RabbitMQ', 'rabbitmq_broker_id')
rabbitmq_user = parser.get('RabbitMQ', 'rabbitmq_user')
rabbitmq_password = parser.get('RabbitMQ', 'rabbitmq_password')
aws_region = parser.get('RabbitMQ', 'aws_region')
rabbitmq_queue_name = parser.get('RabbitMQ', 'rabbitmq_queue_name')

# AWS S3
aws_s3_access_key = parser.get('AWS_S3', 'access_key')
aws_s3_access_secret = parser.get('AWS_S3', 'access_secret')
aws_s3_bucket_name = parser.get('AWS_S3', 'bucket_name')

