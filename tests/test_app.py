import unittest
from unittest.mock import patch, call
import app


class Test(unittest.TestCase):

    @patch('requests.get')
    def test_test_proxy(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.elapsed.total_seconds.return_value = 1
        self.assertEqual(app.test_proxy('207.246.78.234:80'), {'working': True, 'response_time': 1})
        mock_get.side_effect = Exception('Connection Error')
        self.assertEqual(app.test_proxy('207.246.78.234:80'), {'working': False, 'response_time': None })

    def test_is_valid(self):
        self.assertTrue(app.is_valid('207.246.78.249:80'))
        self.assertFalse(app.is_valid('207.246.78.299:80'))

    def test_geo_db_reader(self):
        self.assertEqual(app.geo_db_reader('207.246.78.2:80'), {'region': 'North America'})
        self.assertEqual(app.geo_db_reader(''), {'region': 'error'})

    @patch('app.geo_db_reader')
    @patch('app.test_proxy')
    def test_process_ip(self, mock_geo, mock_proxy):
        proxy = '207.246.78.2:80'
        mock_geo.return_value = {'region': 'Europe' }
        mock_proxy.return_value = { 'working': True, 'proxy': proxy }
        result = {
            'region': 'Europe',
            'working': True, 'proxy': proxy
        }
        self.assertEqual(app.process_ip(proxy), result)
        self.assertEqual(app.process_ip('207.246.78.300:80'), {'invalid': True, 'proxy': '207.246.78.300:80'})

    @patch('app.process_ip')
    @patch('builtins.open', create=True)
    def test_file_handler(self, mock_open, mock_ip):
        mock_open.side_effect = [
            unittest.mock.mock_open(read_data='3.86.30.40:3128').return_value
        ]
        mock_ip.return_value = {'region': 'Europe','working': True, 'proxy':'207.246.78.2:80'}
        result = [{'region': 'Europe','working': True, 'proxy': '207.246.78.2:80'}]
        self.assertEqual(app.file_handler('dev/null'), result)
        

if __name__ == "__main__":
    unittest.main()
