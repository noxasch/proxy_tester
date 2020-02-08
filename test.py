import unittest
from unittest.mock import patch, call
import app


class Test(unittest.TestCase):
    def test_is_valid(self):
        self.assertTrue(app.is_valid('207.246.78.249:80'))
        self.assertFalse(app.is_valid('207.246.78.299:80'))
    
    @patch('builtins.print')
    def test_process_ip(self, mock):
        app.process_ip('')
        assert mock.calls, [call('Invalid proxy')]

    @patch('app.test_proxy')
    def test_process_ip(self, mock):
        app.process_ip('207.246.78.2:80')
        app.process_ip('207.246.78.299:80')
        assert mock.called, [True, True]

    @patch('builtins.print')
    def test_geo_db_reader(self, mock_print):
        app.geo_db_reader('207.246.78.2:80')
        assert mock_print.calls, [call('Europe')]

    @patch('builtins.print')
    @patch('requests.get')
    def test_test_proxy(self, mock_get, mock_print):
        mock_get.return_value.status_code = 200
        mock_get.side_effect = Exception('Connection Error')
        app.test_proxy('207.246.78.234:80')
        app.test_proxy('207.246.78.234:80')
        assert mock_print.calls, [call('Proxy is working'), call('The proxy is down')]


if __name__ == "__main__":
    unittest.main()
