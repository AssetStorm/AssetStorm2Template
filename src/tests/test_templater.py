# -*- coding: utf-8 -*-
from templater import app
import unittest
import responses
import json


class FlaskViewTestCase(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True

    def test_request_content_not_json(self):
        with app.test_client() as test_client:
            response = test_client.post('/', data="foo: 'bar'")
            answer = response.get_json()
            self.assertEqual(400, response.status_code)
        self.assertIn("error", answer)
        self.assertEqual("The supplied data is not a string in JSON format.", answer["error"])

    def test_request_content_no_type(self):
        with app.test_client() as test_client:
            response = test_client.post('/', data='{"tree": {"foo": "bar"}}')
            answer = response.get_json()
            self.assertEqual(400, response.status_code)
        self.assertIn("error", answer)
        self.assertEqual("The supplied data is not a valid tree from AssetStorm.", answer["error"])

    @responses.activate
    def test_successful_conversion(self):
        templates = {
            "article": "<div class=\"article\">{{for(blocks)}}{{blocks}}{{endfor}}</div>",
            "para": "<p>{{text}}</p>",
            "list": "<ul>{{for(items)}}<li>{{items}}</li>{{endfor}}</ul>"
        }
        for type_name in templates.keys():
            responses.add(responses.GET, "https://assetstorm.pinae.net/get_template?type_name=" +
                          type_name + "&template_type=test", status=200, body=templates[type_name])
        with app.test_client() as test_client:
            response = test_client.post('/', data=json.dumps({"template_type": "test", "tree": {
                "type": "article",
                "blocks": [
                    {"type": "para", "text": "Foo sentence."},
                    {"type": "list", "items": ["a", "b", "c"]},
                    {"type": "para", "text": "Bar sentence."}
                ]
            }}))
            self.assertEqual('text/plain', response.mimetype)
            self.assertIn('Content-Type', response.headers)
            self.assertEqual('text/plain; charset=utf-8', response.headers.get('Content-Type'))
            answer = str(response.data, encoding='utf-8')
            self.assertEqual(200, response.status_code)
        self.assertEqual('<div class="article">' +
                         '<p>Foo sentence.</p>' +
                         '<ul><li>a</li><li>b</li><li>c</li></ul>' +
                         '<p>Bar sentence.</p>' +
                         '</div>', answer)
