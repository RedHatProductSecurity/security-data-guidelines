# security-data-guidelines
A set of documents detailing Red Hat's publishing of security data.


## Docs Development

To run a locally served docs site, run:

```
python3 -m venv --system-site-packages venv
source venv/bin/activate
pip install -r requirements/docs-requirements.txt
mkdocs serve
```

We use the `system-site-packages` flag to allow koji to find the python3-rpm package installed via DNF.

If you're running on MacOS and experience issues with the `cairo` dependency, try adding the following:

```
brew install cairo
```
