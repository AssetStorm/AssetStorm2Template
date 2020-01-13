# -*- coding: utf-8 -*-
from flask import Flask, request, Response
from typing import Union
import json
app = Flask(__name__)


def build_json_response(content: Union[dict, list], status=200) -> Response:
    response = app.response_class(
        response=json.dumps(content),
        status=status,
        mimetype='application/json'
    )
    return response


@app.route("/", methods=['POST'])
def template():
    try:
        tree = json.loads(request.get_data(as_text=True))
    except json.JSONDecodeError:
        return build_json_response({"error": "The supplied data is not a string in JSON format."}, status=400)
    return build_json_response({"foo": 2})


if __name__ == "__main__":  # pragma: no mutate
    app.run()
