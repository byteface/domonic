"""
    domonic.JSON
    ====================================
"""

import json
import csv

from domonic.html import table, td, tr, th
# from domonic.javascript import Array


def return_json(func):
    """ decorate any function to return json instead of a python obj """
    def JSON_decorator(*args, **kwargs):
        return json.dumps(func(*args, **kwargs))
    return JSON_decorator


class JSON(object):
    """ A class containing JSON utils """

    def __init__(self):
        pass

    @staticmethod
    def parse_file(filepath: str):
        f = open(filepath)
        data = json.load(f)
        f.close()
        return data

    @staticmethod
    def parse(json_string):
        return json.loads(json_string)

    @staticmethod
    def stringify(data, filepath: str = None, **kwargs):
        if filepath is not None:
            json.dump(data, filepath, **kwargs)
            return json.dumps(data, **kwargs)
        return json.dumps(data, **kwargs)  # indent=4, sort_keys=True, default=str

    @staticmethod
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

        if type(arr) == str: arr = json.loads(arr)  # leniency. allow for a string
        if type(arr) == dict: arr = arr[next(iter(arr))]  # leniency. allow for a dict wrapping a list
        if type(arr) != list: raise ValueError  # if it aint a list by now reject it

        t = table()
        headings = _get_headings(arr, t)
        for item in arr:
            row = tr(''.join([str(td(item.get(heading, ""))) for heading in headings]))
            t.appendChild(row)
        return t

    @staticmethod
    def csvify(arr, outfile="data.csv"):
        """csvify

        takes a json array and dumps a csv file

        Args:
            arr (list): the json array
            outfile (list): the output file

        Returns:
            str: a csv file
        """
        if type(arr) == str: arr = json.loads(arr)  # leniency. allow for a string
        if type(arr) == dict: arr = arr[next(iter(arr))]  # leniency. allow for a dict wrapping a list
        if type(arr) != list: raise ValueError  # if it aint a list by now reject it

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

    @staticmethod
    def csv2json(csv_filepath, json_filepath=None):
        '''
        convert a CSV to JSON.
        '''
        items = []
        with open(csv_filepath, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            for row in csvReader:
                items.append(row)

        if json_filepath is None: return json.dumps(items)

        with open(json_filepath, 'w', encoding='utf-8') as f:
            f.write(json.dumps(items, indent=4))
            return json.dumps(items)

    '''
    @staticmethod
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

    @staticmethod
    def flatten(b, delim="__"):
        '''
        # i.e. input = map( lambda x: JSON.flatten( x, "__" ), input )
        '''
        val = {}
        for i in b.keys():
            if isinstance(b[i], dict):
                get = JSON.flatten(b[i], delim)
                for j in get.keys():
                    val[i + delim + j] = get[j]
            else:
                val[i] = b[i]

        return val

    # def flatten(): # completely flatten. underscore by default or based on rule
    # def nest(): # completely nest. underscore by default or based on rule
    # def purify # remove all the data leaving just the data structure/schema

    @staticmethod
    def is_JSON(json: str):
        if type(json) != str: return False

        if json.startswith('{') and json.endswith('}'):
            return True

        if json.startswith('[') and json.endswith(']'):
            return True

        return False

    # def value(self, query:str):
        # pass


'''
# ideas....

# with JSON( data, 'items') as item:
    # print(item)
    # print(item.id)

# iterator = JSON( data, 'items.age', lambda i: i<30 )

# diff
# merge
# strip('key') .
# format / minify
# json2sql
# json2sqlalchemymodel . i.e. https://www.jsonutils.com/
# csvify_stream for bigger ones.
'''
