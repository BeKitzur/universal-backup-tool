import boto3

from uploaders.uploader import Uploader

S3_OPTIONS = ['bucket', 'aws_access_key_id', 'aws_secret_access_key']


class S3Uploader(Uploader):
    def __init__(self, bucket, aws_access_key_id,
                 aws_secret_access_key, aws_region=None):
        self.aws_region = aws_region
        self.bucket = bucket
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def upload(self, options, path):
        print("Uploading...")
        data = open(path, 'rb')
        s3 = boto3.resource('s3',
                            aws_access_key_id=self.aws_access_key_id,
                            aws_secret_access_key=self.aws_secret_access_key)
        bucket = s3.Bucket(self.bucket)
        bucket.put_object(Key=path, Body=data)
        data.close()

    @classmethod
    def from_dict(cls, dictionary):
        uploader = cls(None, None, None)

        for opt in S3_OPTIONS:
            if opt in dictionary:
                setattr(uploader, opt, dictionary[opt])
        return uploader
