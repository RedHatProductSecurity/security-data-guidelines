# security-data-guidelines
A set of documents detailing Red Hat's publishing of security data.


## Docs Development

To run a locally served docs site, run:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/docs-requirements.txt
mkdocs serve
```

If your running on MacOS and experience issues with the `cairo` dependency, try adding the following:

```
brew install cairo
```
