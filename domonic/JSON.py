"""
    domonic.JSON
    ====================================
"""

import json
import csv

from domonic.html import table, td, tr, th
from domonic.decorators import as_json


return_json = as_json  # legacy. use the one in decorators package


def parse_file(filepath: str):
    """[loads a json file and returns a python object]

    Args:
        filepath (str): [path to json file]

    Returns:
        [type]: [a python object]
    """
    f = open(filepath)
    data = json.load(f)
    f.close()
    return data


def parse(json_string: str):
    """[take a json string and return a python object]

    Args:
        json_string (str): [a json string]

    Returns:
        [type]: [a python object]
    """
    return json.loads(json_string)


def stringify(data, filepath: str = None, **kwargs):
    """[stringify a python object]

    Args:
        data ([type]): [the python object]
        filepath (str, optional): [an optional filepath to save the stringified object] [default: None]

    Returns:
        [type]: [the stringified object]
    """
    if filepath is not None:
        json.dump(data, filepath, **kwargs)
        return json.dumps(data, **kwargs)
    return json.dumps(data, **kwargs)  # indent=4, sort_keys=True, default=str


def tablify(arr):
    """tablify

    takes a json array and returns a html table
    # TODO - reverse. table to json

    Args:
        arr (list): the json array

    Returns:
        str: a html table
    """
    def _get_headings(arr, t):
        headings = []
        row = tr()
        for each in arr:
            for key in each:
                if key not in headings:
                    headings.append(key)
                    row.appendChild(th(key))
        t.appendChild(row)
        return headings

    # print( type(arr) )

    if isinstance(arr, str):
        arr = json.loads(arr)
    if isinstance(arr, dict):
        arr = [arr]
    if type(arr) != list:
        raise ValueError  # need to pass a list of dicts [{},{}]

    t = table()
    headings = _get_headings(arr, t)
    for item in arr:
        # row = tr([td(item.get(heading, "")) for heading in headings]) # incorrect
        row = tr(*[td(item.get(heading, "")) for heading in headings])  # correct
        t.appendChild(row)
    return t


def csvify(arr, outfile="data.csv"):
    """csvify

    takes a json array and dumps a csv file

    Args:
        arr (list): the json array
        outfile (list): the output file

    Returns:
        str: a csv file
    """
    if isinstance(arr, str):
        arr = json.loads(arr)  # leniency. allow for a string
    elif isinstance(arr, dict):
        arr = [arr]
    if type(arr) != list:
        raise ValueError  # if it aint a list by now reject it

    def _get_headings(arr):
        headings = []
        for each in arr:
            for key in each:
                if key not in headings:
                    headings.append(key)
        return headings

    with open(outfile, "w") as file:
        output = csv.writer(file)
        output.writerow(_get_headings(arr))
        for row in arr:
            output.writerow(row.values())


def csv2json(csv_filepath, json_filepath=None):
    '''
    convert a CSV to JSON.
    '''
    items = []
    with open(csv_filepath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            items.append(row)

    if json_filepath is None:
        return json.dumps(items)

    with open(json_filepath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(items, indent=4))
        return json.dumps(items)


'''
def csv2json_hugefile(arr, infile="data.csv", start_row=0):

    def _load_data(csv_fname):
        with open(csv_fname, "r", encoding="latin-1") as records:
            for row in csv.reader(records):
                yield row

    items = iter(load_data(infile))
    headings = next(companies)

    for i in range(start_row):
        next(companies)

    for item in items:
        # TODO - streamwrite to json file.
'''


def flatten(b, delim="__"):
    '''
    # i.e. input = map( lambda x: JSON.flatten( x, "__" ), input )
    '''
    val = {}
    for i in b.keys():
        if isinstance(b[i], dict):
            get = flatten(b[i], delim)
            for j in get.keys():
                val[i + delim + j] = get[j]
        else:
            val[i] = b[i]

    return val


def is_json(json: str) -> bool:
    if type(json) != str:
        return False

    if json.startswith('{') and json.endswith('}'):
        return True

    if json.startswith('[') and json.endswith(']'):
        return True

    return False
