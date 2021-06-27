## Examples

Some of these examples require additional packages to be installed.

To be able to run all the examples install everything in requirements-dev.txt


### install extra packages

```bash
cd /domonoic
. venv/bin/activate
python3 -m pip install -r requirements-dev.txt
python3 -m pip install domonic --upgrade
```

### Running examples

Make sure to enable your virtual env. Then cd to the folder and run it

```bash
. venv/bin/activate
cd examples/
python lifecalendar.py
```

or if its in a nested folder...

```bash
. venv/bin/activate
cd examples/events
python events.py
```
