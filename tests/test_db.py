import os
import flog
import unittest
import tempfile
from flog import app
from flog.models.models import init_db

class FlogTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a blank temp database before each test"""
        self.db_fd, flog.database = tempfile.mkstemp()
        self.app = flog.app.test_client()
        with app.app_context():
            init_db()

    def tearDown(self):
        """Destroy blank temp database after each test"""
        os.close(self.db_fd)
        os.unlink(flog.database)

    def test_db(self):
        test = os.path.exists(flog.database)
        self.assertTrue(test)

    def test_connect(self):
        """
        Connect to database
        """
        self.assertIsNotNone(self.db_fd)

if __name__ == '__main__' :
    unittest.main()