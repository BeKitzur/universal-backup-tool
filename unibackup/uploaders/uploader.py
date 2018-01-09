from abc import ABCMeta, abstractclassmethod


class Uploader(metaclass=ABCMeta):

    @abstractclassmethod
    def upload(self, options):
        pass


def create(targets_list, name):
    uploader = None
    target = None

    for t in targets_list:
        if t['name'] == name:
            target = t
            break

    if target['type'] == 's3':
        from .s3 import S3Uploader
        uploader = S3Uploader.from_dict(target)

    return uploader
