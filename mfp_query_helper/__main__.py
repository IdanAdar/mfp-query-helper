from utils import FilterParameters, ESConfig, DateUtils, QueryNotFoundError
from query_engine import run_query, Queries
from elasticsearch.exceptions import ConnectionError, NotFoundError
import argparse
import re


def validate_date_argument(value, end_date=False):
    '''
    Returns the date timestamp of a string of the format year,month,date i.e. 2014,4,24,
    or another timestamp. All timestamps are represented in epoch time in milliseconds

    Timestamps will just be normalized to 13 digits for milliseconds, strings will be converted

    default date timestamp for string values are the timestamp for 12:00:00 AM
    if end_date is True, timestamp will be for 11:59:59 PM
    '''
    # regex to match date string year,month,day
    if re.match('^\d{4},\d{1,2},\d{1,2}$', value):
        year, month, day = value.split(',')
        if end_date:
            return DateUtils.get_day_timestamp_end(year, month, day)
        else:
            return DateUtils.get_day_timestamp_start(year, month, day)

    # or try to parse timestamp
    int_value = None
    try:
        int_value = int(value)
    except ValueError:
        return False

    # normalize timestamp to 13 digit epoch
    if len(value) < 10:
        return False
    elif len(value) == 10:
        return str(int_value*1000)
    elif len(value) == 11:
        return str(int_value*100)
    elif len(value) == 12:
        return str(int_value*10)
    elif len(value) == 13:
        return value
    else:
        return False


def main():
    parser = argparse.ArgumentParser(description='MFP Query Helper')
    parser.add_argument('query', help='Name of the query you want to run. Available queries are: {0}'.format(', '.join(Queries.ALL_QUERIES)))
    parser.add_argument('-esHost', help=(
        'Host configuration for Elasticsearch. The default is localhost:9500. '
        'Please use format <host>:<port>'))
    parser.add_argument('-esIndex', help='Elasticseach index to seach on. The default is worklight.')
    parser.add_argument('--mfpAppName', help='MFP app name to filter on')
    parser.add_argument('--mfpAppVersion', help='MFP version name to filter on')
    parser.add_argument('--deviceModel', help='Device model to filter on')
    parser.add_argument('--deviceOS', help='Device OS to filter on')
    parser.add_argument('--deviceOSversion', help='Device OS version to filter on')
    parser.add_argument('--startDate', help=(
        'Start date for time ranged filter. This must be used with an endDate and '
        'must be in the format \'year,month,day\''))
    parser.add_argument('--endDate', help=(
        'End date for a time ranged filter. This must be used with a startDate and '
        'must be in the format \'year,month,day\''))

    args = parser.parse_args()

    filter_parameters = FilterParameters()
    filter_parameters.mfp_app_name = args.mfpAppName
    filter_parameters.mfp_app_version = args.mfpAppVersion
    filter_parameters.device_model = args.deviceModel
    filter_parameters.device_os = args.deviceOS
    filter_parameters.device_os_version = args.deviceOSversion

    if (args.startDate and not args.endDate) or (args.endDate and not args.startDate):
        parser.error('startDate and endDate filters must be used together')

    # validate startDate and endDate
    if args.startDate and args.endDate:
        start_date = validate_date_argument(args.startDate)
        if not start_date:
            start_date = parser.error('Invalid startDate {0}. Use epoch timestamp or date string like 2015,4,24'.format(args.startDate))

        end_date = validate_date_argument(args.endDate, True)
        if not end_date:
            end_date = parser.error('Invalid endDate {0}. Use epoch timestamp or date string like 2015,4,24'.format(args.endDate))

        filter_parameters.start_date = start_date
        filter_parameters.end_date = end_date

    es_config = ESConfig()

    if args.esHost:
        host, port = args.esHost.split(':')
        if host is None or port is None:
            parser.error('Invalid Elasticsearch host {0}. Please use the format <host>:<port>'.format(args.esHost))

        es_config.host = host
        es_config.port = port

    if args.esIndex:
        es_config.index = args.esIndex

    try:
        run_query(args.query, filter_parameters, es_config)
    except QueryNotFoundError:
        print('No query named {0}. Available queries are: {1}'.format(args.query, ', '.join(Queries.ALL_QUERIES)))
    except ConnectionError:
        print('Could not connect to {0}'.format(es_config.get_full_host()))
    except NotFoundError as e:
        print('Error running query: {0}'.format(e))

if __name__ == '__main__':
    main()