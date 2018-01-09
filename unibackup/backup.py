import os
import shutil
from . import dumpers
from . import uploaders

config = None
backupers_list = []
dumpers_dict = {}
uploaders_dict = {}


class Backuper:
    dump_name = None

    def __init__(self, dumper, uploader, options):
        self.dumper = dumper
        self.uploader = uploader
        self.options = options

    def backup(self):
        self.options.update(self.dumper.dump(self.options))
        self.uploader.upload(self.options)
        self.clean()

    @classmethod
    def from_dict(cls, dictionary):
        dumper_name = dictionary['source']
        if dumper_name in dumpers_dict:
            dumper = dumpers_dict[dumper_name]
        else:
            dumper = dumpers.create(config['sources'], dumper_name)
            dumpers_dict[dumper_name] = dumper

        uploader_name = dictionary['target']
        if uploader_name in uploaders_dict:
            uploader = uploaders_dict[uploader_name]
        else:
            uploader = uploaders.create(config['targets'], uploader_name)
            uploaders_dict[uploader_name] = dumper

        backuper = Backuper(dumper, uploader, dictionary)
        return backuper

    def clean(self):
        try:
            os.remove(self.options['out_name'])
        except IsADirectoryError:
            shutil.rmtree(self.options['out_name'])


def run():
    for bd in config['backups']:
        backuper = Backuper.from_dict(bd)
        backupers_list.append(backuper)

    for backuper in backupers_list:
        backuper.backup()
