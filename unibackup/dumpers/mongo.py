import subprocess
import util
from dumpers.dumper import Dumper

MONGODUMP_OPTIONS = ['host', 'port', 'username', 'password',
                     'db', 'collection', 'query', 'archive', 'out', 'gzip']


def get_out_name(options):
    out_name = ""
    out_prefix = ""
    if 'out_prefix' in options:
        out_prefix = options['out_prefix']
    else:
        for o in ['source', 'db', 'collection']:
            if o in options:
                out_prefix += "{}-".format(options[o])

    out_name += out_prefix
    out_name += util.get_date(options['date_format'])
    if ('archive' in options and options['archive']) \
            and ('gzip' in options and options['gzip']):
        out_name += '.gz'

    return {"out_name": out_name,
            "out_prefix": out_prefix}


def option_string(opt, arg):
    if arg is True:
        return "--{}".format(opt)
    else:
        return "--{}={}".format(opt, arg)


class MongoDumper(Dumper):
    def __init__(self, host, port=27017, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def dump(self, options):
        out_name_dict = get_out_name(options)
        out_name = out_name_dict['out_name']
        options = self.build_option_list(options, out_name)

        print("Dumping...")
        print(options)
        subprocess.run(['mongodump'] + options)
        return out_name_dict

    @classmethod
    def from_dict(cls, dictionary):
        dumper = cls(None)

        for opt in MONGODUMP_OPTIONS:
            if opt in dictionary:
                setattr(dumper, opt, dictionary[opt])
        return dumper

    def build_option_list(self, options, out_name):
        options_list = []

        for opt in MONGODUMP_OPTIONS:
            if opt in ['archive', 'out']:
                continue

            if hasattr(self, opt):
                arg = getattr(self, opt)
            elif opt in options:
                arg = options[opt]
            else:
                continue

            if arg:
                options_list.append(option_string(opt, arg))

        if 'archive' in options and options['archive']:
            out_option = 'archive'
        else:
            out_option = 'out'
        options_list.append(option_string(out_option, out_name))

        return options_list

