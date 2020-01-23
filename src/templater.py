# -*- coding: utf-8 -*-
from flask import Flask, request, Response
from typing import Union
from tree_processor import TreeProcessor, IllegalAssetStormStructureError
import json
import os
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
        request_payload = json.loads(request.get_data(as_text=True))
    except json.JSONDecodeError:
        return build_json_response({"error": "The supplied data is not a string in JSON format."}, status=400)
    if "tree" not in request_payload:
        return build_json_response({"error": "The supplied json data needs to have a 'tree' key " +
                                             "with the AssetStorm tree."}, status=400)
    tree = request_payload["tree"]
    if "template_type" in request_payload.keys():
        template_type = request_payload["template_type"]
    else:
        template_type = os.getenv("TEMPLATE_TYPE", "proof_html")
    if "assetstorm_url" in request_payload.keys():
        assetstorm_url = request_payload["assetstorm_url"]
    else:
        assetstorm_url = os.getenv("ASSETSTORM_URL", "https://assetstorm.pinae.net")
    tp = TreeProcessor(asset_storm_url=assetstorm_url, template_type=template_type)
    try:
        rendered_template = tp.run(tree)
    except IllegalAssetStormStructureError:
        return build_json_response({"error": "The supplied data is not a valid tree from AssetStorm."}, status=400)
    return build_text_response(rendered_template)


@app.route("/live", methods=['GET'])
def live():
    return build_text_response("", status=200)


if __name__ == "__main__":  # pragma: no mutate
    app.run()  # pragma: no cover
