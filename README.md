MFP Query Helper
================

The MFP Query Helper command line program helps extract information from MFP Analytics that cannot be done in
version 7.1

This tool depends on python 2.7

Installation
------------

To install globally:

```
$ sudo python setup.py install
```

To uninstall globally, use the uninstall.sh script with root:

```
$ sudo sh uninstall.sh
```

Or you can create a python virtual environment and install it there. Make sure the virtual environment uses
python 2.7

```
$ virtualenv venv
$ . venv/bin/activate
$ python setup.py install
```

Basic Usage
-----------
```
$ mfp_query_helper -h
```

Currently, there are 3 queries that are supported: newDevices, mfpAppVersions, and distinctMfpAppVersions

To run one simply use:

```
$ mfp_query_helper <query_name>
```

By default, this will search Elasticsearch host localhost:9500 on index 'worklight'

Command Line Arguments
----------------------

There are command line arguments for Elasticsearch configuration, and to filter the given queries

#### Elasticsearch config

To change the Elasticsearch host to query, use -esHost:

```
$ mfp_query_helper -esHost myhost.com:9500
```

To change the index to query, use -esIndex:

```
$ mfp_query_helper -esIndex otherindex
```


#### Filtering

You can filter any query by app name, app version, device model, device os, device os version, and time range.

A basic filter would look like:

```
$ mfp_query_helper <query_name> --mfpAppName myApp --mfpAppVersion 1.0
```

To filter on time range, use --startDate and --endDate arugments. These can either be epoch timestamps, or date
strings of the format year,month,date i.e. 2014,4,24. Both startDate and endDate need to be used together.

```
$ mfp_query_helper <query_name> --startDate 2014,1,1 --endDate 2014,2,1
```

To get a full list of the command line arguments, run

```
$ mfp_query_helper -h
```