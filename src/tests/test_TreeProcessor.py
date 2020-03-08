# -*- coding: utf-8 -*-
from tree_processor import TreeProcessor, IllegalAssetStormStructureError
import unittest
import responses


class TreeProcessorTestCast(unittest.TestCase):
    def test_get_template_from_cache(self):
        tp = TreeProcessor()
        tp.template_cache = {
            "foo": "<x>{{a}}</x><y>{{for(b)}}<z>{{b}}</z>{{endfor}}</y>"
        }
        template = tp.get_template("foo")
        self.assertEqual("<x>{{a}}</x><y>{{for(b)}}<z>{{b}}</z>{{endfor}}</y>", template)

    @responses.activate
    def test_get_template_from_request(self):
        mock_test_url = "https://assetstorm.example.com"
        responses.add(
            responses.GET,
            mock_test_url + "/get_template?type_name=foo&template_type=proof_html",
            status=200,
            body="<x>{{a}}</x><y>{{for(b)}}<z>{{b}}</z>{{endfor}}</y>"
        )
        tp = TreeProcessor(asset_storm_url=mock_test_url)
        template = tp.get_template("foo")
        self.assertEqual("<x>{{a}}</x><y>{{for(b)}}<z>{{b}}</z>{{endfor}}</y>", template)
        self.assertIn("foo", tp.template_cache.keys())

    def test_no_type_in_request(self):
        tp = TreeProcessor()
        self.assertRaises(IllegalAssetStormStructureError, tp.run, {"a": "123"})

    def test_run_no_recursion(self):
        tp = TreeProcessor()
        tp.template_cache = {
            "foo": "<x>{{a}}</x><y>{{for(b)}}<z>{{b}}</z>{{endfor}}</y>"
        }
        res = tp.run({
            "type": "foo",
            "a": "123",
            "b": ["56", "89", "08", "15"]
        })
        self.assertEqual("<x>123</x><y><z>56</z><z>89</z><z>08</z><z>15</z></y>", res)

    def test_run(self):
        tp = TreeProcessor()
        tp.template_cache = {
            "foo": "<x>{{a}}</x><y>{{for(b)}}<z>{{b}}</z>{{endfor}}</y>{{for(c)}}[{{c}}]{{endfor}}",
            "bar": "<div>{{a}} - {{b}}</div>",
            "baz": "{{{x}}}"
        }
        res = tp.run({
            "type": "foo",
            "a": {
                "type": "bar",
                "a": "xyz",
                "b": "https://foo.bar/baz"
            },
            "b": ["56", "89", "08", "15"],
            "c": [
                {"type": "baz", "x": "1"},
                {"type": "baz", "x": "2"},
                {"type": "baz", "x": "3"}
            ]
        })
        self.assertEqual("<x><div>xyz - https://foo.bar/baz</div></x>" +
                         "<y><z>56</z><z>89</z><z>08</z><z>15</z></y>" +
                         "[{1}][{2}][{3}]", res)

    def test_paragraphs_with_numbering(self):
        tp = TreeProcessor()
        tp.template_cache = {
            "article": "<article>{{for(content)}}{{content}}{{endfor}}</article>",
            "paragraph": "<p id=\"{{$id}}\">{{text}}</p>",
            "code": "<code>{{x}}</code>"
        }
        res = tp.run({
            "type": "article",
            "content": [
                {'type': 'paragraph', 'text': 'Foo'},
                {'type': 'code', 'x': 'print(x)'},
                {'type': 'paragraph', 'text': 'Bar'}
            ]
        })
        self.assertEqual("<article><p id=\"e0\">Foo</p><code>print(x)</code><p id=\"e1\">Bar</p></article>", res)

    def test_python_code_block(self):
        tp = TreeProcessor(template_type="sy_xml")
        tp.template_cache = {
            "article": "<article>{{for(content)}}{{content}}{{endfor}}</article>",
            "paragraph": "<p id=\"{{$id}}\">{{text}}</p>",
            "code": "{{highlight_sy_xml(code)}}"
        }
        res = tp.run({
            "type": "article",
            "content": [
                {"type": "paragraph", "text": "Para 1"},
                {"type": "code", "language": "python", "code": "a = 4\nprint(3.2 + a)"},
                {"type": "paragraph", "text": "Para 2"}
            ]
        })
        self.assertEqual("<article><p id=\"e0\">Para 1</p><codeblock coding_language=\"python\">" +
                         "a <operator>=</operator> <number>4</number>\n" +
                         "<builtin>print</builtin><punctuation>(</punctuation>" +
                         "<number>3.2</number> <operator>+</operator> a<punctuation>)</punctuation>" +
                         "</codeblock><p id=\"e1\">Para 2</p></article>", res)
