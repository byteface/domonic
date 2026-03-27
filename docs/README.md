# domonic docs

If something is missing, unclear, or wrong, feel free to send a pull request.

To build locally:

```bash
python3 -m pip install -r requirements-docs.txt
cd docs
make html
```

The built site will end up in `docs/_build/html/`.

Read the Docs uses:

- [docs/conf.py](./conf.py)
- [../.readthedocs.yaml](../.readthedocs.yaml)
