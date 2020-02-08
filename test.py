import unittest
from app import geo_db_reader
from app import is_valid
from app import process_ip 
from app import test_proxy


class Test(unittest.TestCase):
    def test_is_valid(self):
        self.assertEqual(is_valid('207.246.78.249:80'), True)
        self.assertEqual(is_valid('207.246.78.299:80'), False)

if __name__ == "__main__":
    unittest.main()
    