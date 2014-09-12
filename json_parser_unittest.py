import unittest
import json_parser
import json

class ParserTestCase(unittest.TestCase):
    """Tests for `primes.py`."""

    def test_appIsRunning(self):
        """appIsRunning should return false if stopped status and true if started status"""
        self.assertFalse(json_parser.appIsRunning("STOPPED"))
        self.assertTrue(json_parser.appIsRunning("STARTED"))

    def test_findAppNameMatch(self):
        """findAppNameMatch should return false if no match is found and true if a match is found"""
        self.assertFalse(json_parser.findAppNameMatch("sample-zdd", "sample-zdd-123"))
        self.assertTrue(json_parser.findAppNameMatch("sample-zdd", "sample-zdd-ef306b2479a7ecd4337875b4d954a4c8fc18e237"))

    def test_iterateJson(self):
        """iterateJson should return notfound if no matches in jsonobj
        or return a pipe delimited string of values if it finds a match in the jsonobj"""
        validString = """{
          "resources": [{
            "entity": {
              "name": "sample-zdd-ef306b2479a7ecd4337875b4d954a4c8fc18e237",
              "memory": 1028,
              "instances": 1,
              "disk_quota": 1024,
              "state": "STARTED"
            }
          }]
        }"""
        invalidState = """{
          "resources": [{
            "entity": {
              "name": "sample-zdd-ef306b2479a7ecd4337875b4d954a4c8fc18e237",
              "memory": 1028,
              "instances": 1,
              "disk_quota": 1024,
              "state": "STOPPED"
            }
          }]
        }"""

        self.assertEqual(json_parser.iterateJson("sample-zdd", json.loads("{}")), "notfound", "invalid json should return notfound value")
        self.assertEqual(json_parser.iterateJson("nomatch-value",  json.loads(validString)), "notfound", "no match should return notfound value")
        self.assertEqual(json_parser.iterateJson("sample-zdd",  json.loads(invalidState)), "notfound", "no match should return notfound value")
        self.assertEqual(json_parser.iterateJson("sample-zdd",  json.loads(validString)), "sample-zdd-ef306b2479a7ecd4337875b4d954a4c8fc18e237|1|1028|1024","valid json should return the pipe delimeted values we need")

if __name__ == '__main__':
    unittest.main()
