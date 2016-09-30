from datetime import datetime
import calendar
import time

class Config(object):
    def __init__(self, cli_args):
        # defaults
        self.host = 'localhost'
        self.port = '9500'
        self.index = 'worklight'
        self.timeout = 10
        self.scroll_size = 10000
        self.debug = False

        if cli_args.esHost:
            host, port = cli_args.esHost.split(':')
            if host is None or port is None:
                parser.error('Invalid Elasticsearch host {0}. Please use the format <host>:<port>'.format(cli_args.esHost))

        self.host = host
        self.port = port

        if cli_args.esIndex:
            self.index = cli_args.esIndex

        if cli_args.timeout:
            self.timeout = cli_args.timeout

        if cli_args.scroll_size:
            self.scroll_size = cli_args.scroll_size

        if cli_args.debug:
            self.debug = True

    def get_full_host(self):
        return '{0}:{1}'.format(self.host, self.port)


class FilterParameters(object):
    def __init__(self):
        self.mfp_app_name = None
        self.mfp_app_version = None
        self.device_model = None
        self.device_os = None
        self.device_os_version = None
        self.start_date = None
        self.end_date = None


    def build_filter(self):
        if not any([self.mfp_app_name, self.mfp_app_version, self.device_model,
                self.device_os, self.device_os_version,
                self.start_date and self.end_date]):
            return None

        must_clauses = []

        if self.mfp_app_name:
            must_clauses.append(self._new_term('mfpAppName', self.mfp_app_name))

        if self.mfp_app_version:
            must_clauses.append(self._new_term('mfpAppVersion', self.mfp_app_version))

        if self.device_model:
            must_clauses.append(self._new_term('deviceModel', self.device_model))

        if self.device_os:
            must_clauses.append(self._new_term('deviceOS', self.device_os))

        if self.device_os_version:
            must_clauses.append(self._new_term('deviceOSversion', self.device_os_version))

        filter_obj = {}
        if must_clauses:
            filter_obj['bool'] = {
                'must': must_clauses
            }

        return filter_obj

    def build_query(self):
        if not any([self.start_date and self.end_date]):
            return None

        filtered_query_obj = {}
        range_filter = None
        if self.start_date and self.end_date:
            range_filter = {
                'firstAccessTimestamp': {
                    'from': self.start_date,
                    'to': self.end_date,
                    'include_lower': True,
                    'include_upper': True
                }
            }

        if range_filter:
            filtered_query_obj['range'] = range_filter

        return filtered_query_obj

    def build_filtered_query(self):
        query_obj = {}

        filtered_query_obj = self.build_query()
        filter_obj = self.build_filter()
        '''Apply queries and filters'''
        if filter_obj and filtered_query_obj:
            query_obj['query'] = {
                'filtered': {
                    'query': filtered_query_obj,
                    'filter': filter_obj
                }
            }
        elif filter_obj:
            query_obj['query'] = {
                'filtered': {
                    'query': filter_obj
                }
            }
        else:
            query_obj['query'] = {
                'match_all': {}
            }

        return query_obj

    def _new_term(self, name, value):
        '''Creates a term object for filters'''
        return {
            'term': {
                name: value
            }
        }

    def __str__(self):
        data = {
            'mfpAppName': self.mfp_app_name,
            'mfpAppVersion': self.mfp_app_version,
            'deviceModel': self.device_model,
            'deviceOS': self.device_os,
            'deviceOSversion': self.device_os_version,
            'startDate': self.start_date,
            'endDate': self.end_date,
        }
        return str(data)


class DateUtils(object):
    @staticmethod
    def get_day_timestamp_gmt(d):
        '''Returns the epoch timestamp in milliseconds of the beginning
        of the given day in GMT'''
        return calendar.timegm((d.year, d.month, d.day, 0, 0, 0))*1000

    @staticmethod
    def get_day_timestamp_start(year, month, day):
        year, month, day = int(year), int(month), int(day)
        return int(time.mktime(datetime(year, month, day, 0, 0, 0).timetuple())*1000)

    @staticmethod
    def get_day_timestamp_end(year, month, day):
        year, month, day = int(year), int(month), int(day)
        return int(time.mktime(datetime(year, month, day, 23, 59, 59).timetuple())*1000)


class MfpUtils(object):
    @staticmethod
    def version_less_than(base, other):
        base = base.split('.')
        other = other.split('.')

        if len(base) < len(other):
            for i in range(len(other) - len(base)):
                base.append(0)
        elif len(other) < len(base):
            for i in range(len(base) - len(other)):
                other.append(0)

        # print(base, other)

        for i in range(len(base)):
            if int(base[i]) < int(other[i]):
                return True

        return False

class QueryNotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
