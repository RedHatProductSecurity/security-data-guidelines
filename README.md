# security-data-guidelines
A set of documents detailing Red Hat's publishing of security data.

## Development

Install python environment and dependencies:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/docs-requirements.txt
```

## Docs Development

To run a locally served docs site, run:

```
mkdocs serve
```

If you're running on MacOS and experience issues with the `cairo` dependency, try adding the following:

```
brew install cairo
```

## Tests

Validate SPDX examples
```
tox spdx-schema
```

Validate CycloneDX examples
```
tox cdx-schema
```