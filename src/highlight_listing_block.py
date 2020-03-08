# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import requests
import os
import re


def flat_tree_replacements(tree: ET.Element, replacement_function: callable) -> ET.Element:
    i = 0
    if tree.text is not None:
        sp, ne = replacement_function(tree.text)
        if len(ne) > 0:
            tree.text = sp
            for nec, new_elem in enumerate(ne):
                tree.insert(0 + nec, new_elem)
            i += len(ne)
    while i < len(tree):
        leaf = tree[i]
        if leaf.tail is not None:
            sp, ne = replacement_function(leaf.tail)
            if len(ne) > 0:
                leaf.tail = sp
                for nec, new_elem in enumerate(ne):
                    tree.insert(i + 1 + nec, new_elem)
                i += len(ne)
        i += 1
    return tree


def replace_from_regex(matches: re.Match, element_tag: str) -> (str, ET.Element):
    str_part = matches.group(1)
    new_elem = ET.Element(element_tag)
    new_elem.text = matches.group(2)
    new_elem.tail = matches.group(3)
    return str_part, new_elem


def python_replacements(tree: ET.Element) -> ET.Element:
    def replace_builtins(s: str) -> (str, list):
        re_list = [r"^([\s\S]*)(print|setattr|frozenset)(\([\s\S]*)$",
                   r"^([\s\S]*)(abs|all|any|ascii|bin|bool|breakpoint|bytearray|bytes|callable|chr|" +
                   r"classmethod|compile|complex|delattr|dict|dir|divmod|enumerate|eval|exec|filter|" +
                   r"float|format|getattr|globals|hasaattr|hash|help|hex|id|input|int|" +
                   r"isinstance|issubclass|iter|len|list|locals|map|max|memoryview|min|next|object|oct|" +
                   r"open|ord|pow|property|range|repr|reversed|round|set|slice|sorted|" +
                   r"staticmethod|str|sum|super|tuple|type|vars|zip|__import__)(\([\s\S]*)$"]
        i = 0
        matches = re.match(re_list[i], s)
        while not matches and i < len(re_list):
            matches = re.match(re_list[i], s)
            i += 1
        new_elems = []
        while matches:
            s, last_new_elem = replace_from_regex(matches, "builtin")
            new_elems.insert(0, last_new_elem)
            i = 0
            matches = re.match(re_list[i], s)
            while not matches and i < len(re_list):
                matches = re.match(re_list[i], s)
                i += 1
        return s, new_elems

    return flat_tree_replacements(tree, replace_builtins)


def operator_and_punctuation_replacements(tree: ET.Element) -> ET.Element:
    def replace_operator(s: str) -> (str, list):
        re_list = [r"^([\s\S]*)(&lt;=|&gt;=|<=|>=)([\s\S]*)$",
                   r"^([\s\S]*)(=|<|&lt;|>|&gt;|!=|\+|-)([\s\S]*)$"]
        i = 0
        matches = re.match(re_list[i], s)
        while not matches and i < len(re_list):
            matches = re.match(re_list[i], s)
            i += 1
        new_elems = []
        while matches:
            s, last_new_elem = replace_from_regex(matches, "operator")
            new_elems.insert(0, last_new_elem)
            i = 0
            matches = re.match(re_list[i], s)
            while not matches and i < len(re_list):
                matches = re.match(re_list[i], s)
                i += 1
        return s, new_elems

    def replace_punctuation(s: str) -> (str, list):
        regex = r"^([\s\S]*)(\(|\)|\[|\]|\{|\}|,|:|\.)([\s\S]*)$"
        matches = re.match(regex, s)
        new_elems = []
        while matches:
            s, last_new_elem = replace_from_regex(matches, "punctuation")
            new_elems.insert(0, last_new_elem)
            matches = re.match(regex, s)
        return s, new_elems

    tree = flat_tree_replacements(tree, replace_operator)
    tree = flat_tree_replacements(tree, replace_punctuation)
    return tree


def highlight_sy_xml(lang: str, code: str) -> str:
    rt = {
        "string": "string",
        "number": "number",
        "keyword": "keyword",
        "title": "function"
    }
    strip_list = ["function", "params"]
    lang_specific_replacements = {
        "python": python_replacements
    }

    def replace_highlight_tags(tree: ET.Element) -> ET.Element:
        def append_text(el: ET.Element, addition: str) -> ET.Element:
            if el.text is None:
                el.text = addition
            else:
                el.text += addition
            return el

        def append_tail(el: ET.Element, addition: str) -> ET.Element:
            if el.tail is None:
                el.tail = addition
            else:
                el.tail += addition
            return el

        def insert_tail(el: ET.Element, addition: str) -> ET.Element:
            if el.tail is None:
                el.tail = addition
            else:
                el.tail = addition + el.tail
            return el

        i = 0
        while i < len(tree):
            leaf = tree[i]
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
                if leaf.text is not None:
                    if i > 0:
                        tree[i - 1] = append_tail(tree[i - 1], leaf.text)
                    else:
                        tree = append_text(tree, leaf.text)
                if len(leaf) > 0:
                    for sli, sub_leaf in enumerate(leaf):
                        tree.insert(i + sli, sub_leaf)
                        if sli == len(leaf) - 1 and leaf.tail is not None:
                            sub_leaf = append_tail(sub_leaf, leaf.tail)
                else:
                    if leaf.tail is not None:
                        if i > 0:
                            tree[i - 1] = append_tail(tree[i - 1], leaf.tail)
                        else:
                            tree = insert_tail(tree, leaf.tail)
                tree.remove(leaf)
                i -= 1
            i += 1
        return tree

    highlighter_url = os.getenv("HIGHLIGHT_SERVICE_URL", "http://localhost:3000")
    highlighter_response = requests.post(highlighter_url, json={"lang": lang, "code": code})
    html_highlighted_code = highlighter_response.json()["highlighted_code"]
    tree = ET.fromstring("<codeblock>" + html_highlighted_code + "</codeblock>")
    tree.set('coding_language', lang)
    tree = replace_highlight_tags(tree)
    if lang in lang_specific_replacements.keys():
        tree = lang_specific_replacements[lang](tree)
    tree = operator_and_punctuation_replacements(tree)
    return ET.tostring(tree, encoding='unicode')
