# AWS-RabbitMQ
 Send and Receive RabbitMQ message from AWS. Then upload those to AWS S3 storage. 

#1 YOU NEED config.ini FILE TO RUN IT

Sample file looks like this

    [RabbitMQ]
    rabbitmq_broker_id = xxxxxxxx
    rabbitmq_user = xxxxxxxx
    rabbitmq_password = xxxxxxxx
    aws_region = xxxxxxxx
    rabbitmq_queue_name = xxxxxxxx
    
    [AWS_S3]
    access_key = xxxxxxxx
    access_secret = xxxxxxxx
    bucket_name = xxxxxxxx
