import boto3

from uploaders.uploader import Uploader
from datetime import datetime, timedelta, timezone

S3_OPTIONS = ['bucket', 'aws_access_key_id', 'aws_secret_access_key']


class S3Uploader(Uploader):
    def __init__(self, bucket, aws_access_key_id,
                 aws_secret_access_key, aws_region=None):
        self.aws_region = aws_region
        self.s3 = boto3.resource('s3',
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)
        self.bucket = self.s3.Bucket(bucket)

    def upload(self, options):
        print("Uploading...")
        with open(options['out_name'], 'rb') as data:
            self.bucket.put_object(Key=options['out_name'], Body=data)

        self.clean_old(options)

    @classmethod
    def from_dict(cls, dictionary):
        bucket = dictionary['bucket']
        aws_access_key_id = dictionary['aws_access_key_id']
        aws_secret_access_key = dictionary['aws_secret_access_key']

        aws_region = None
        if 'aws_region' in dictionary:
            aws_region = dictionary['aws_region']

        return cls(bucket, aws_access_key_id, aws_secret_access_key, aws_region)

    def clean_old(self, options):
        retention = None
        if 'retention' in options:
            retention = options['retention']

        if retention['type'] == 'time_retention':
            seconds, minutes, hours, days, weeks = 0, 0, 0, 0, 0
            if 'seconds' in retention: seconds = retention['seconds']
            if 'minutes' in retention: minutes = retention['minutes']
            if 'hours' in retention: hours = retention['hours']
            if 'days' in retention: days = retention['days']
            if 'weeks' in retention: weeks = retention['weeks']

            retention_time = timedelta(seconds=seconds, minutes=minutes,
                                       hours=hours, days=days, weeks=weeks)
            most_old_time = datetime.now(timezone.utc) - retention_time

            object_summary_iterator = self.bucket.objects.filter(
                Prefix=options['out_prefix']
            )
            objects_to_delete = []
            for obj in object_summary_iterator:
                if obj.last_modified < most_old_time:
                    print("Deleting old object {}".format(obj.key))
                    objects_to_delete.append({'Key': obj.key})

            if not objects_to_delete:
                return

            delete_response = self.bucket.delete_objects(
                Delete={
                    'Objects': objects_to_delete
                }
            )
