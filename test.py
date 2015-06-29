from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
import unittest

host = 'localhost'
port = 9500

index = 'worklight'
doc_type = 'Devices'

def check_es(cls):
    if not hasattr(cls, 'es'):
        cls.fail('Could not connect to elasticsearch')

def delete_devices_from_es(es):
    es.delete_by_query(index=index, doc_type=doc_type,
        body={'query': {'match_all': {} }})

class TestNewDevices(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        es = None
        try:
            self.es = Elasticsearch(
                    hosts=[{'host': host, 'port': port}],
                    sniff_on_start=True
                )
        except TransportError:
            pass

    def test_new_devices(self):
        check_es(self)
        delete_devices_from_es(self.es)

        # index 2 different Devices on 2 different days
        self.es.index(index=index, doc_type=doc_type,
            body={
                'appID': '',
                'firstAccessTimestamp': '',
                'mfpAppName': '',
                'mfpAppVersion': '',
                'deviceID': '',
                'deviceModel': '',
                'deviceOS': '',
                'deviceOSversion': ''
            })

        self.es.index(index=index, doc_type=doc_type,
            body={
                'appID': '',
                'firstAccessTimestamp': '',
                'mfpAppName': '',
                'mfpAppVersion': '',
                'deviceID': '',
                'deviceModel': '',
                'deviceOS': '',
                'deviceOSversion': ''
            })

if __name__ == '__main__':
    print 'THIS WILL DELETE DOCUMENTS ON ELASTICSEACH {0}:{1}'.format(host, port)

    msg = 'Do you still want to continue [Y/n]? '
    user_input = raw_input(msg).lower()

    while(user_input != '' and user_input != 'y' and user_input != 'n'):
        user_input = raw_input(msg)

    if user_input == '' or user_input == 'y':
        unittest.main()