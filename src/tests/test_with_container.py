# -*- coding: utf-8 -*-
from templater import app
import unittest
import json


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.as_url = "http://localhost:8081"

    def test_raw_template_title(self):
        tree = {'assetstorm_url': self.as_url,
                'template_type': 'raw',
                'tree': {'type': 'block-heading', 'heading': 'Titel'}
                }
        with app.test_client() as test_client:
            response = test_client.post('/', data=json.dumps(tree, ensure_ascii=False).encode('utf-8'))
            self.assertEqual('text/plain', response.mimetype)
            self.assertIn('Content-Type', response.headers)
            self.assertEqual('text/plain; charset=utf-8', response.headers.get('Content-Type'))
            answer = str(response.data, encoding='utf-8')
            self.assertEqual(200, response.status_code)
        self.assertEqual("Titel\n\n", answer)


if __name__ == '__main__':
    unittest.main()
