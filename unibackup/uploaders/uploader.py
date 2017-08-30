from abc import ABCMeta, abstractclassmethod
import uploaders


class Uploader(metaclass=ABCMeta):

    @abstractclassmethod
    def upload(self, options, path):
        pass


def create(targets_list, name):
    uploader = None
    target = None

    for t in targets_list:
        if t['name'] == name:
            target = t
            break

    if target['type'] == 's3':
        uploader = uploaders.S3Uploader.from_dict(target)

    return uploader
