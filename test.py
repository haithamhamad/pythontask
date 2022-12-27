import unittest
import requests
import json
import app


class Testapp(unittest.TestCase):
    def test_is_json(self):
        res=app.get_DB("cpu","all")
        json.dumps(res)
        y=[{ "date":"2022-12-26 12:27:30","used":"1.07%"}]
        json.dumps(y)
        self.assertEqual(y,res)
          



if __name__ == '__main__':
    unittest.main()



