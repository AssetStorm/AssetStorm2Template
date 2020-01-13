# -*- coding: utf-8 -*-
from tree_processor import TreeProcessor
import unittest


class TreeProcessorTestCast(unittest.TestCase):
    def test_get_template_from_cache(self):
        tp = TreeProcessor()
        tp.template_cache = {
            "foo": "<x>{{a}}</x><y>{{for(b)}}<z>{{b}}</z>{{endfor}}</y>"
        }
        template = tp.get_template("foo")
        self.assertEqual("<x>{{a}}</x><y>{{for(b)}}<z>{{b}}</z>{{endfor}}</y>", template)

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
