import boto3
from .aws_env import *

class App():
    def __init__(self, session, bucket, queue):
        self.session = session
        self.bucket = bucket
        self.queue = queue

def smart_setup():
    bucket = S3.Bucket(BUCKET_NAME)
    bucket.load()
    if(bucket.creation_date is None):
        bucket.create(ACL='public-read')
        # Define the configuration rules
        cors_configuration = {
            'CORSRules': [{
                'AllowedHeaders': ['Authorization'],
                'AllowedMethods': ['GET', 'PUT', 'POST'],
                'AllowedOrigins': ['*'],
                'ExposeHeaders': ['GET', 'PUT', 'POST'],
                'MaxAgeSeconds': 3000
            }]
        }

        # Set the CORS configuration
        cors = bucket.Cors()
        cors.put(CORSConfiguration=cors_configuration)
    try:
        queue = SQS.get_queue_by_name(QueueName=SQS_NAME)
    except:
        queue = SQS.create_queue(
            QueueName=SQS_NAME,
            Attributes={
                'ReceiveMessageWaitTimeSeconds':"20",
                'DelaySeconds': '0',
                'VisibilityTimeout': "100"
            }
        )
    return App(AWS, bucket, queue)

def delete_all(app:App):
    for key in app.bucket.objects.all():
        key.delete()
    app.bucket.delete()
    app.queue.delete()