import unittest
from app import geo_db_reader
from app import is_valid
from app import process_ip 
from app import test_proxy


class Test(unittest.TestCase):
    def test_is_valid(self):
        self.assertTrue(is_valid('207.246.78.249:80'))
        self.assertFalse(is_valid('207.246.78.299:80'))

if __name__ == "__main__":
    unittest.main()
