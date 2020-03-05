import unittest
from highlight_listing_block import highlight_sy_xml


class HighlighterTestCase(unittest.TestCase):
    def test_python_sy_xml(self):
        code = "​print(\"foo\")\n" + \
               "for i in range(2):\n" + \
               "  if i < 1:\n" + \
               "    foo_bar = [x.baz(3.2) for x in enumerate({\"a\": 1, 'b': dict()}.keys())]\n" + \
               "def aaabc(x: int, y: str) -> list:\n" + \
               "  return [x, y]\n" + \
               "aaabc(2, \"3\")\n" + \
               "value = type(r\"2\") is bytes\n"
        self.assertEqual(
            "<codeblock coding_language=\"python\">\n" +
            "<keyword>print</keyword><punctuation>(</punctuation>" +
            "<string>\"foo\"</string><punctuation>)</punctuation>\n" +
            "<keyword>for</keyword> i <keyword>in</keyword> " +
            "<builtin>range</builtin><punctuation>(</punctuation><number>2</number>" +
            "<punctuation>)</punctuation><punctuation>:</punctuation>\n" +
            "  <keyword>if</keyword> i <operator>&lt;</operator> <number>1</number><punctuation>:</punctuation>\n" +
            "    foo_bar <operator>=</operator> <punctuation>[</punctuation>" +
            "x<punctuation>.</punctuation>baz<punctuation>(</punctuation><number>3.2</number>" +
            "<punctuation>)</punctuation> <keyword>for</keyword> x <keyword>in</keyword> " +
            "<builtin>enumerate</builtin><punctuation>(</punctuation><punctuation>{</punctuation>" +
            "<string>\"a\"</string><punctuation>:</punctuation> <number>1</number>" +
            "<punctuation>,</punctuation> <string>'b'</string><punctuation>:</punctuation> " +
            "<builtin>dict</builtin><punctuation>(</punctuation><punctuation>)</punctuation>" +
            "<punctuation>}</punctuation><punctuation>.</punctuation>keys" +
            "<punctuation>(</punctuation><punctuation>)</punctuation><punctuation>)</punctuation>" +
            "<punctuation>]</punctuation>\n" +
            "<keyword>def</keyword> <function>aaabc</function><punctuation>(</punctuation>" +
            "x<punctuation>:</punctuation> <builtin>int</builtin>" +
            "<punctuation>,</punctuation> y<punctuation>:</punctuation> <builtin>str</builtin>" +
            "<punctuation>)</punctuation> <operator>-</operator><operator>&gt;</operator> <builtin>list</builtin>" +
            "<punctuation>:</punctuation>\n" +
            "<keyword>return</keyword> <punctuation>[</punctuation>x<punctuation>,</punctuation> y" +
            "<punctuation>]</punctuation>\n" +
            "aaabc<punctuation>(</punctuation><number>2</number><punctuation>,</punctuation> <string>\"3\"</string>" +
            "<punctuation>)</punctuation>\n" +
            "value <operator>=</operator> <builtin>type</builtin><punctuation>(</punctuation>r<string>\"2\"</string>" +
            "<punctuation>)</punctuation> <keyword>is</keyword> <builtin>bytes</builtin>\n" +
            "</codeblock>", highlight_sy_xml("python", code))


if __name__ == '__main__':
    unittest.main()
