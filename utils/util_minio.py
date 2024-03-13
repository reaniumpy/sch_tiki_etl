import boto3

def get_s3_resource():
    s3 = boto3.resource('s3',
                        endpoint_url='http://localhost:9000',
                        aws_access_key_id='ROOTNAME',
                        aws_secret_access_key='CHANGEME123',
                        config=boto3.session.Config(signature_version='s3v4'))

    return s3