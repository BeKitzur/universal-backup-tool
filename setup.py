from setuptools import setup
from setuptools import find_packages

setup(
        name="unibackup",
        version="0.1.0",
        packages=find_packages(),
        description="unibackup (universal backup) is a tool \
                     for doing backups easily.",

        install_requires=[
            'docopt',
            'pyyaml',
            'boto3'
        ],

        python_requires='>=3',

        entry_points={
            'console_scripts': [
                'unibackup = unibackup.main:main']
        }
)
