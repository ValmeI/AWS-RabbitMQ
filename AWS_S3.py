import boto3
import os
from app_logging import logObject

'# what is Amazon Kinesis Data Firehose and maybe use that in future?'

# basic S3 client connection


class AwsS3Client:

    def __init__(self, access_key, access_secret):
        try:
            self.client = boto3.client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=access_secret
            )

        except Exception as e:
            logObject.warning(e)

# inherit connection info, in case download method and so on is added later


class S3Actions(AwsS3Client):

    def upload_s3_file(self, filename_with_path, bucket_name, file_name, upload_folder):
        folder_and_filename = f'{upload_folder}/{file_name}'
        # if file does not exist rase exception else try uploading it to S3
        if os.path.exists(filename_with_path) is False:
            raise logObject.warning(Exception('File not found'))

        else:
            try:
                self.client.upload_file(filename_with_path,
                                        bucket_name,
                                        folder_and_filename
                                        )
                logObject.warning('        File upload to S3 Successful')

            except Exception as e:
                logObject.warning(e)
