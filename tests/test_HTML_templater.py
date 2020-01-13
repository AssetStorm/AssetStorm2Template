# -*- coding: utf-8 -*-
from HTML_templater import app
import unittest


class ConvertTestCase(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True

    def test_request_content_not_json(self):
        with app.test_client() as test_client:
            response = test_client.post('/', data="foo: 'bar'")
            answer = response.get_json()
            self.assertEqual(400, response.status_code)
        self.assertIn("error", answer)
        self.assertEqual("The supplied data is not a string in JSON format.", answer["error"])
