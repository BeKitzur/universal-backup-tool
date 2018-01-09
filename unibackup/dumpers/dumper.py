from abc import ABCMeta, abstractclassmethod


class Dumper(metaclass=ABCMeta):
    @abstractclassmethod
    def dump(self, options):
        pass


def create(sources_list, name):
    dumper = None
    source = None

    for s in sources_list:
        if s['name'] == name:
            source = s
            break

    if source['type'] == 'mongodb':
        from .mongo import MongoDumper
        dumper = MongoDumper.from_dict(source)

    return dumper
