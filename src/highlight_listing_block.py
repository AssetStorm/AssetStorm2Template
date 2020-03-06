# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import requests
import os


def highlight_sy_xml(lang: str, code: str) -> str:
    rt = {
        "string": "string",
        "number": "number",
        "keyword": "keyword"
    }
    strip_list = ["function"]

    def replace_highlight_tags(tree: ET) -> ET:
        for leaf in tree:
            print(leaf.tag, leaf.get('class'))
            if leaf.tag == 'span' and leaf.get('class').startswith('hljs-') and leaf.get('class')[5:] in rt.keys():
                sub_leafs = [sl for sl in leaf]
                new_tag = rt[leaf.get('class')[5:]]
                text = leaf.text
                tail = leaf.tail
                leaf.clear()
                leaf.text = text
                leaf.tail = tail
                leaf.tag = new_tag
                if len(sub_leafs) > 0:
                    leaf.extend(sub_leafs)
                    replace_highlight_tags(leaf)
            elif leaf.tag == 'span' and leaf.get('class').startswith('hljs-') and leaf.get('class')[5:] in strip_list:
                pass  # remove tag an insert child tags in its place
        return tree

    highlighter_url = os.getenv("HIGHLIGHT_SERVICE_URL", "http://localhost:3000")
    highlighter_response = requests.post(highlighter_url, json={"lang": lang, "code": code})
    html_highlighted_code = highlighter_response.json()["highlighted_code"]
    tree = ET.fromstring("<codeblock>" + html_highlighted_code + "</codeblock>")
    tree.set('coding_language', lang)
    tree = replace_highlight_tags(tree)
    return ET.tostring(tree, encoding='unicode')
