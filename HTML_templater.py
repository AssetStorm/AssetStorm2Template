# -*- coding: utf-8 -*-
from flask import Flask, request, Response
from typing import Union
from tree_processor import TreeProcessor, IllegalAssetStormStructureError
import json
app = Flask(__name__)


def build_json_response(content: Union[dict, list], status: int = 200) -> Response:
    response = app.response_class(
        response=json.dumps(content),
        status=status,
        mimetype='application/json'
    )
    return response


def build_text_response(content: str, status: int = 200) -> Response:
    response = app.response_class(
        response=content,
        status=status,
        mimetype='text/plain'
    )
    return response


@app.route("/", methods=['POST'])
def template():
    try:
        tree = json.loads(request.get_data(as_text=True))
    except json.JSONDecodeError:
        return build_json_response({"error": "The supplied data is not a string in JSON format."}, status=400)
    tp = TreeProcessor()
    try:
        rendered_template = tp.run(tree)
    except IllegalAssetStormStructureError:
        return build_json_response({"error": "The supplied data is not a valid tree from AssetStorm."}, status=400)
    return build_text_response(rendered_template)


if __name__ == "__main__":  # pragma: no mutate
    app.run()  # pragma: no cover
