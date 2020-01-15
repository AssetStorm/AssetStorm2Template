# AssetStorm2HTML
AssetStorm to HTML templating microservice

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