Disclaimer
==========
I have only copied this over to public git as the employee who originally authored this has left. No support can be provided.

MFP Query Helper
================

The MFP Query Helper command line program helps extract information from MFP Analytics version 7.1

This tool depends on python 2.7

Installation
------------

To install the mfp_query_helper CLI:

$ sudo python setup.py install

To uninstall (on unix systems), use the uninstall.sh script with root:

$ sudo sh uninstall.sh

You can also create a python virtual environment, if you do not wish to install globally.
Make sure the virtual environment uses python 2.7

$ virtualenv venv
$ . venv/bin/activate
$ python setup.py install

Preparing your cluser for querying
----------------------------------
The Elasticsearch http endpoint must be enabled for the tool to query your datastore.
To enable to the http endpoint, add the JNDI property “analytics/http.enabled” to your
cluster with value “true”.

Basic Usage
-----------
$ mfp_query_helper -h

Currently, there are 3 queries that are supported: newDevices, mfpAppVersions, and distinctMfpAppVersions.

To run one simply use:

$ mfp_query_helper <query_name>

By default, this will search Elasticsearch host localhost:9500 on index 'worklight'.

Query Information
-----------------
- newDevices
    The newDevices query returns an array of new devices per day. A device is considered
    new the first time it connects to your MFP server.

    Response payload looks like
    [
        {
            'date': 0000000000, // timestamp of day
            'count': 0 // number of new devices on that day
        },
        ...
    ]
- mfpAppVersions
    The mfpAppVersions query returns a count of all devices that have connected to a
    an MFP application. An MFP application is considered a unique combination of app
    name and app version.

    Response payload looks like
    {
        'AppName1': {
            '1.0': 20,
            '2.0': 25,
            ...
        },
        ...
    }

    It is important to note that if a device connects to AppName1 version 1.0 and version
    2.0, it is counted in both. If you would like distinct devices, use distinctMfpAppVersions
    query.
- distinctMfpAppVersions
    The distinctMfpAppVersions query returns a count of unique devices that have connected
    to an MFP application. An MFP application is considered a unique combination of app
    name and app version. For this query, the latest app version will be used.

    For example, if a device connects to AppName1 versions 1.0, 2.0 and 3.0, it will only
    be counted in version 3.0.

    Response payload looks like
    {
        'AppName1': {
            '1.0': 20,
            '2.0': 25,
            ...
        },
        ...
    }

Command Line Arguments
----------------------

There are command line arguments for Elasticsearch configuration, and to filter the given queries

Usage:
```
usage: mfp_query_helper [-h] [-esHost ESHOST] [-esIndex ESINDEX]
                        [--mfpAppName MFPAPPNAME]
                        [--mfpAppVersion MFPAPPVERSION]
                        [--deviceModel DEVICEMODEL] [--deviceOS DEVICEOS]
                        [--deviceOSversion DEVICEOSVERSION]
                        [--startDate STARTDATE] [--endDate ENDDATE]
                        [--timeout TIMEOUT] [--scroll_size SCROLL_SIZE]
                        [--debug]
                        query

MFP Query Helper

positional arguments:
  query                 Name of the query you want to run. Available queries
                        are: newDevices, mfpAppVersions,
                        distinctMfpAppVersions

optional arguments:
  -h, --help            show this help message and exit
  -esHost ESHOST        Host configuration for Elasticsearch. The default is
                        localhost:9500. Please use format <host>:<port>
  -esIndex ESINDEX      Elasticseach index to seach on. The default is
                        worklight.
  --mfpAppName MFPAPPNAME
                        MFP app name to filter on
  --mfpAppVersion MFPAPPVERSION
                        MFP version name to filter on
  --deviceModel DEVICEMODEL
                        Device model to filter on
  --deviceOS DEVICEOS   Device OS to filter on
  --deviceOSversion DEVICEOSVERSION
                        Device OS version to filter on
  --startDate STARTDATE
                        Start date for time ranged filter. This must be used
                        with an endDate and must be in the format
                        'year,month,day'
  --endDate ENDDATE     End date for a time ranged filter. This must be used
                        with a startDate and must be in the format
                        'year,month,day'
  --timeout TIMEOUT     Operation timeout in seconds. Defaults to 10
  --scroll_size SCROLL_SIZE
                        Size for each scroll while querying. Defaults to
                        10,000
  --debug
  ```

Elasticsearch config
--------------------

To change the Elasticsearch host to query, use -esHost:

$ mfp_query_helper -esHost myhost.com:9500

To change the index to query, use -esIndex:

$ mfp_query_helper -esIndex otherindex

Filtering
---------

You can filter any query by app name, app version, device model, device os, device os version, and time range.

A basic filter would look like:

$ mfp_query_helper <query_name> --mfpAppName myApp --mfpAppVersion 1.0

The keys for filtering are as follows
- mfpAppName
- mfpAppVersion
- deviceModel
- deviceOS
- deviceOSversion

Time range filter use
- startDate
- endDate

startDate and endDate parameters can be epoch timestamps or date strings of the format
year,month,date (i.e. 2014,4,24). Both startDate and endDate need to be used together.

$ mfp_query_helper <query_name> --startDate 2014,1,1 --endDate 2014,2,1

Other
-----

There are a few other command line arguments for greater control over the queries

- timeout: operation timeout for the query
- scroll_size: number of documents to fetch at a time using the Elasticsearch scroll API
- debug: enables more debug output

Troubleshooting
---------------

If you are running into issues run the same query with the --debug flag. This should give you more output and
help to determine what the problem is. If the query is timing out, inscrease the timeout duration using the
--timeout argument. If the Python program is running out of memory (MemoryError), try adjusting the --scroll_size.
More information about scrolling is below.

How the query works below with the scroll API:

The Elasticsearch scroll API allows you to "scan" through every document from any index and type efficiently. We use this
API in this tool to query all of the Devices documents. This means that each scroll iteration is bringing scroll_size number
of documents into memory, and iterating over them. Depending on the query and the number of Devices documents you have,
this could cause the Python interpretor to run out of memory. Try tweaking the scroll_size parameter when this happens.

Some Examples
-------------

To get all new devices for the app "Insurance App" with Elasticsearch running on mysite.com, port 9500, index myindex

$ mfp_query_helper newDevices -esHost mysite.com:9500 -esIndex myindex --mfpAppName "Insurance App"
