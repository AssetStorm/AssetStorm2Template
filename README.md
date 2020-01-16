# AssetStorm2Template
AssetStorm to HTML templating microservice

## Usage
This microservice can be configured by the following
environment variables:
 *  `TEMPLATE_TYPE : str` - That's the key for the
    template the templater asks AssetStorm for.
 *  `ASSETSTORM_URL : str` - That's the url of the
    AssetStorm backend service. The templater will
    apped the path, just give the base url.
    
This Flask application is meant to be used as a
microservice in a container. Deploy it like any 
other Flask app. 
 
## Running the tests
The tests use `pytest`. You can install `pytest` 
with pip: `pip install pytest`.

Run all tests with: `python -m pytest`

You may also generate coverage reports with 
`coverage.py` (`pip install coverage`). Generate
html reports with:

```bash
coverage run --omit="env/*,tests/*" -m pytest
coverage html
```

With `coverage report` you get some additional 
statistics.