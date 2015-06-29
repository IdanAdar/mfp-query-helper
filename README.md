MFP Query Helper
================

The MFP Query Helper command line program helps extract information from MFP Analytics that cannot be done in
version 7.1

This tool depends on python 2.7

Installation
------------

To install globally:

```bash
$ sudo python setup.py install
```

To uninstall globally, use the uninstall.sh script with root:

```bash
$ sudo sh uninstall.sh
```

Or you can create a python virtual environment and install it there. Make sure the virtual environment uses
python 2.7

```bash
$ virtualenv venv
$ . venv/bin/activate
$ python setup.py install
```

Basic Usage
-----------

```bash
$ mfp_query_helper -h
```

Currently, there are 3 queries that are supported: newDevices, mfpAppVersions, and distinctMfpAppVersions

To run one simply use:

```bash
$ mfp_query_helper [query]
```

By default, this will search Elasticsearch host localhost:9500 on index 'worklight'

Queries
-------

##### newDevices

This query will return an array of JSON objects, representing a date where new devices connected
to the MobileFirst Platform

```javascript
[{'count': 2, 'date': 1435536000000}]
```

##### mfpAppVersions

This query will return a JSON object of the total count of all combinations of MFP Apps and versions.
This means if a device updated MyApp version 1.0 to 2.0, it will be counted in both versions

```javascript
{
    'MyApp': {
        '1.0': 2,
        '2.0': 5
    },
    'OtherApp': {
        '1.0': 10
    }
}
```

##### distinctMfpAppVersions

This query will return a JSON object of the distinct count of all combinations of MFP Apps and versions.
This means if a device updates MyApp version 1.0 to 2.0, it will only be counted in version 2.0

```javascript
{
    'MyApp': {
        '1.0': 1,
        '2.0': 2
    },
    'OtherApp': {
        '1.0': 10
    }
}
```

Command Line Arguments
----------------------

There are command line arguments for Elasticsearch configuration, and to filter the given queries

#### Elasticsearch config

To change the Elasticsearch host to query, use -esHost:

```bash
$ mfp_query_helper -esHost myhost.com:9500
```

To change the index to query, use -esIndex:

```bash
$ mfp_query_helper -esIndex otherindex
```

#### Filtering

You can filter any query by app name, app version, device model, device os, device os version, and time range.

A basic filter would look like:

```bash
$ mfp_query_helper [query] --mfpAppName myApp --mfpAppVersion 1.0
```

To filter on time range, use --startDate and --endDate arugments. These can either be epoch timestamps, or date
strings of the format year,month,date i.e. 2014,4,24. Both startDate and endDate need to be used together.

```bash
$ mfp_query_helper [query] --startDate 2014,1,1 --endDate 2014,2,1
```

To get a full list of the command line arguments, run

```bash
$ mfp_query_helper -h
```