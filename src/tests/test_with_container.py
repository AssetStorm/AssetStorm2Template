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

    def test_standard_article_proof_html(self):
        article = {
            'type': 'article-standard',
            'x_id': '1234567890123456789',
            'catchphrase': 'Testartikel',
            'column': 'Wissen',
            'working_title': 'Standard-Testartikel',
            'title': 'Titel',
            'subtitle': 'Untertitel',
            'teaser': 'Vorlauftext',
            'author': 'Pina Merkert',
            'content': [
                {'type': 'block-paragraph', 'spans': [
                    {'type': 'span-regular', 'text': 'Text des Artikels.'}]},
                {'type': 'block-paragraph', 'spans': [
                    {'type': 'span-regular', 'text': 'Mehrere Absätze'}]}],
            'article_link': {'link': {'type': 'span-ct-link'},
                             'link_description': 'Dokumentation',
                             'type': 'article-link-container'},
            'bibliography': []}
        tree = {'assetstorm_url': self.as_url,
                'template_type': 'proof_html',
                'tree': article}
        with app.test_client() as test_client:
            response = test_client.post('/', data=json.dumps(tree, ensure_ascii=False).encode('utf-8'))
            self.assertEqual('text/plain', response.mimetype)
            self.assertIn('Content-Type', response.headers)
            self.assertEqual('text/plain; charset=utf-8', response.headers.get('Content-Type'))
            answer = str(response.data, encoding='utf-8')
            self.assertEqual(200, response.status_code)
        self.assertEqual(
            "<article-standard>" +
            "<x_id>1234567890123456789</x_id>" +
            "<catchphrase>Testartikel</catchphrase>" +
            "<magazine-column>Wissen</magazine-column>" +
            "<h1>Titel</h1>" +
            "<h2 class=\"subtitle\">Untertitel</h2>" +
            "<teaser>Vorlauftext</teaser>" +
            "<author>Von Pina Merkert</author>" +
            "<p>Text des Artikels.</p><p>Mehrere Absätze</p>" +
            "<article-link><article-link-description>Dokumentation:</article-link-description> " +
            "<ctlink /></article-link>" +
            "<div class=\"bibliography\"><h3>Literatur</h3><ol></ol></div>" +
            "</article-standard>", answer)

    def test_standard_article_markdown(self):
        article = {
            'type': 'article-standard',
            'x_id': '1234567890123456789',
            'catchphrase': 'Testartikel',
            'column': 'Wissen',
            'working_title': 'Standard-Testartikel',
            'title': 'Titel',
            'subtitle': 'Untertitel',
            'teaser': 'Vorlauftext',
            'author': 'Pina Merkert',
            'content': [
                {'type': 'block-paragraph', 'spans': [
                    {'type': 'span-regular', 'text': 'Text des Artikels.'}]},
                {'type': 'block-paragraph', 'spans': [
                    {'type': 'span-regular', 'text': 'Mehrere Absätze'}]}],
            'article_link': {'link': {'type': 'span-ct-link'},
                             'link_description': 'Dokumentation',
                             'type': 'article-link-container'},
            'bibliography': [
                {'type': 'bibliography-reference-ct-intern',
                 'author': 'Max Mustermann',
                 'title': 'Referenzartikel',
                 'subtitle': 'So kann es aussehen',
                 'issue': '13',
                 'year': '19',
                 'page': '173'},
                {'type': 'bibliography-reference-web',
                 'url': 'https://example.com'}
            ]}
        tree = {'assetstorm_url': self.as_url,
                'template_type': 'markdown',
                'tree': article}
        with app.test_client() as test_client:
            response = test_client.post('/', data=json.dumps(tree, ensure_ascii=False).encode('utf-8'))
            self.assertEqual('text/plain', response.mimetype)
            self.assertIn('Content-Type', response.headers)
            self.assertEqual('text/plain; charset=utf-8', response.headers.get('Content-Type'))
            answer = str(response.data, encoding='utf-8')
            self.assertEqual(200, response.status_code)
        self.assertEqual(
            "<!---\ntype: article-standard\nx_id: 1234567890123456789\ncatchphrase: Testartikel\ncolumn: Wissen\n" +
            "working_title: Standard-Testartikel\ntitle: MD_BLOCK\n-->\n\n" +
            "# Titel\n\n<!---\n" +
            "subtitle: MD_BLOCK\n-->\n\n" +
            "## Untertitel\n\n<!---\n" +
            "teaser: MD_BLOCK\n-->\n\n" +
            "**Vorlauftext**\n\n<!---\n" +
            "author: MD_BLOCK\n-->\n\n" +
            "Pina Merkert\n\n<!---\n" +
            "content: MD_BLOCK\n-->\n\n" +
            "Text des Artikels.\n\nMehrere Absätze\n\n<!---\n" +
            "article_link:\n" +
            "  type: article-link-container\n" +
            "  link_description: Dokumentation\n" +
            "  link: <ctlink />\n" +
            "bibliography:\n" +
            "  - type: bibliography-reference-ct-intern\n" +
            "    author: Max Mustermann\n" +
            "    title: Referenzartikel\n" +
            "    subtitle: So kann es aussehen\n" +
            "    issue: 13\n" +
            "    year: 19\n" +
            "    page: 173\n" +
            "  - type: bibliography-reference-web\n" +
            "    url: https://example.com\n" +
            "-->", answer)

    def get_toc_article(self) -> dict:
        return {
            'type': 'article-table-of-contents',
            'title': 'Inhaltsverzeichnis',
            'x_id': '1234567890123456789',
            'content': [
                {'type': 'toc-block-main', 'entries': [
                    {'type': 'toc-heading-container', 'title': 'Block 1', 'entries': [
                        {'type': 'toc-small', 'spans': [
                            {'type': 'span-strong', 'text': 'Kurztext 1'},
                            {'type': 'span-regular', 'text': ' mit Ergänzung'}
                        ], 'page': '13'},
                        {'type': 'toc-small', 'spans': [
                            {'type': 'span-strong', 'text': 'Kurztext 2'},
                            {'type': 'span-regular', 'text': ' mit Ergänzung'}
                        ], 'page': '17'}
                    ]},
                    {'type': 'toc-small', 'spans': [
                        {'type': 'span-strong', 'text': 'Kurztext 3'},
                        {'type': 'span-regular', 'text': ' mit Ergänzung'}
                    ], 'page': '21'},
                    {'type': 'toc-heading-container', 'title': 'Block 2', 'entries': [
                        {'type': 'toc-small', 'spans': [
                            {'type': 'span-strong', 'text': 'Kurztext 4'},
                            {'type': 'span-regular', 'text': ' mit Ergänzung'}
                        ], 'page': '130'},
                        {'type': 'toc-small', 'spans': [
                            {'type': 'span-strong', 'text': 'Kurztext 5'},
                            {'type': 'span-regular', 'text': ' mit Ergänzung'}
                        ], 'page': '134'},
                        {'type': 'toc-small', 'spans': [
                            {'type': 'span-strong', 'text': 'Kurztext 6'},
                            {'type': 'span-regular', 'text': ' mit Ergänzung'}
                        ], 'page': '138'}
                    ]}
                ]}
            ]
        }

    def test_toc_sy_xml(self):
        tree = {'assetstorm_url': self.as_url,
                'template_type': 'sy_xml',
                'tree': self.get_toc_article()}
        with app.test_client() as test_client:
            response = test_client.post('/', data=json.dumps(tree, ensure_ascii=False).encode('utf-8'))
            self.assertEqual('text/plain', response.mimetype)
            self.assertIn('Content-Type', response.headers)
            self.assertEqual('text/plain; charset=utf-8', response.headers.get('Content-Type'))
            answer = str(response.data, encoding='utf-8')
            self.assertEqual(200, response.status_code)
        self.assertEqual(
            "<document dbref=\"1234567890123456789\">\n" +
            "<title>Inhaltsverzeichnis</title>\n" +
            "<textel>\n" +
            "<toc>\n" +
            "<tocentry>\n" +
            "Block 1\n" +
            "<tocentry page=\"13\">\n" +
            "<bold>Kurztext 1</bold> mit Ergänzung\n" +
            "</tocentry>\n" +
            "<tocentry page=\"17\">\n" +
            "<bold>Kurztext 2</bold> mit Ergänzung\n" +
            "</tocentry>\n" +
            "</tocentry>\n" +
            "<tocentry page=\"21\">\n" +
            "<bold>Kurztext 3</bold> mit Ergänzung\n" +
            "</tocentry>\n" +
            "<tocentry>\n" +
            "Block 2\n" +
            "<tocentry page=\"130\">\n" +
            "<bold>Kurztext 4</bold> mit Ergänzung\n" +
            "</tocentry>\n" +
            "<tocentry page=\"134\">\n" +
            "<bold>Kurztext 5</bold> mit Ergänzung\n" +
            "</tocentry>\n" +
            "<tocentry page=\"138\">\n" +
            "<bold>Kurztext 6</bold> mit Ergänzung\n" +
            "</tocentry>\n" +
            "</tocentry>\n" +
            "</toc>\n" +
            "</textel>\n" +
            "</document>", answer)

    def test_toc_markdown(self):
        tree = {'assetstorm_url': self.as_url,
                'template_type': 'markdown',
                'tree': self.get_toc_article()}
        with app.test_client() as test_client:
            response = test_client.post('/', data=json.dumps(tree, ensure_ascii=False).encode('utf-8'))
            self.assertEqual('text/plain', response.mimetype)
            self.assertIn('Content-Type', response.headers)
            self.assertEqual('text/plain; charset=utf-8', response.headers.get('Content-Type'))
            answer = str(response.data, encoding='utf-8')
            self.assertEqual(200, response.status_code)
        self.assertEqual(
            "<!---\ntype: article-table-of-contents\nx_id: 1234567890123456789\ntitle: MD_BLOCK\n-->\n\n" +
            "# Inhaltsverzeichnis\n\n" +
            "<!---\ncontent: MD_BLOCK\n-->\n\n" +
                "<!---\ntype: toc-block\nentries: MD_BLOCK\n-->\n\n" +
                    "<!---\ntype: toc-heading-container\ntitle: Block 1\nentries: MD_BLOCK\n-->\n\n" +
                        "<!---\ntype: toc-small\npage: 13\ntext: MD_BLOCK\n-->\n\n" +
                        "**Kurztext 1** mit Ergänzung\n\n" +
                        "<!--- -->\n\n" +
                        "<!---\ntype: toc-small\npage: 17\ntext: MD_BLOCK\n-->\n\n" +
                        "**Kurztext 2** mit Ergänzung\n\n" +
                        "<!--- -->\n\n" +
                    "<!--- -->\n\n" +
                    "<!---\ntype: toc-small\npage: 21\ntext: MD_BLOCK\n-->\n\n" +
                    "**Kurztext 3** mit Ergänzung\n\n" +
                    "<!--- -->\n\n" +
                    "<!---\ntype: toc-heading-container\ntitle: Block 2\nentries: MD_BLOCK\n-->\n\n" +
                        "<!---\ntype: toc-small\npage: 130\ntext: MD_BLOCK\n-->\n\n" +
                        "**Kurztext 4** mit Ergänzung\n\n" +
                        "<!--- -->\n\n" +
                        "<!---\ntype: toc-small\npage: 134\ntext: MD_BLOCK\n-->\n\n" +
                        "**Kurztext 5** mit Ergänzung\n\n" +
                        "<!--- -->\n\n" +
                        "<!---\ntype: toc-small\npage: 138\ntext: MD_BLOCK\n-->\n\n" +
                        "**Kurztext 6** mit Ergänzung\n\n" +
                        "<!--- -->\n\n" +
                    "<!--- -->\n\n" +
                "<!--- -->\n\n" +
            "<!--- -->", answer)


if __name__ == '__main__':
    unittest.main()
