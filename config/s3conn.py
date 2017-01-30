import boto3
from botocore.client import ClientError
import aws_config as config


def get_s3_bucket(bucket_name):
    s3 = boto3.resource('s3',
                        aws_access_key_id=config.access_id,
                        aws_secret_access_key=config.access_secret
                        )
    try:
        bucket = s3.create_bucket(Bucket=bucket_name,
                                  CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
        return bucket
    except ClientError as e:
        # if the bucket is created will raise this error, return it, else return False
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyOwnedByYou':
            return s3.Bucket(bucket_name)
        else:
            return False


# should replace bucket name here with correct one
def write_file_to_s3(data, key, bucket_name="discursive"):
    bucket = get_s3_bucket(bucket_name)
    if bucket is not False:
        bucket.put_object(Key=key, Body=data)
    else:
        print bucket_name + " bucket could not be found"
