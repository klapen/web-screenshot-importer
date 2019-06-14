import unittest
from resources.Maintenance import Maintenance

class TestMaintenance(unittest.TestCase):
    def test_server_ok(self):
        obj = Maintenance()
        self.assertEqual(obj.get(), { 'status': 'ok', 'version': 'v0.1' }, 'Should return an OK structure')

if __name__ == '__main__':
    unittest.main()
