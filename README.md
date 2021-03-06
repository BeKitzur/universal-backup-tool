# Universal Backup Tool

'Create backups from any sources and push to any target'.

The initial goal is to create a universal backup tool that could create
multiple backups from various sources and store them in various places.

Currently, this tool only supports creating a dump of a MongoDB database and
pushing it to an S3 bucket, and deleting old backups in S3 (see the `retention`
configuration option in the example).

## Install

~~~
python3 setup.py install [--user]
~~~

## Usage

~~~
unibackup [options]

-h --help  Show help
-c <config> --config=<config>  Configuration file
~~~

For example:
~~~
unibackup -c my-backups.yml
~~~

## Configuration file example

~~~
---
sources:
  - name: my-replica-set
    type: mongodb
    host: prod/backend-1.prod,backend-2.prod,backend-3.prod
    port: 27017
    username: username
    password: password
    authenticationDatabase: admin

targets:
  - name: my-aws-bucket
    type: s3
    bucket: my-mongodb-backups
    aws_access_key_id:
    aws_secret_access_key: 

backups:
  - source: my-replica-set
    target: my-aws-bucket
    db: my_database
    gzip: True
    archive: True
    out_prefix: my-database-
    date_format: "%Y%m%dT%H%M%SZ"

    retention:
      type: time_retention
      weeks: 4
~~~
