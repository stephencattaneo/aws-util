import json
import unittest

from pylint import epylint as lint

class TestUtils(unittest.TestCase):
    def test_lint(self):
        (stdout, stderr) = lint.py_run('handler.py', return_std=True)
        errors = json.loads(stdout.read() or '[]')

        try:
            self.assertEqual(len(errors), 0)
        except AssertionError as e:
            stdout.seek(0)
            print(stdout.read())
            raise e

if __name__ == '__main__':
    unittest.main()
