"""
    domonic.utils
    ====================================
    snippets etc
"""
# import typing
import random
from re import sub
from itertools import chain, islice
from collections import Counter

from domonic.decorators import deprecated


class Utils(object):
    """ Utils """

    @staticmethod
    def case_camel(s: str) -> str:
        """ case_camel('camel-case') > 'camelCase' """
        s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
        return s[0].lower() + s[1:]

    @staticmethod
    def case_snake(s: str) -> str:
        """
        snake('camelCase') # 'camel_case'
        """
        return '_'.join(
            sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
            s.replace('-', ' '))).split()).lower()

    @staticmethod
    def case_kebab(s: str) -> str:
        """
        kebab('camelCase') # 'camel-case'
        """
        return '-'.join(
            sub(r"(\s|_|-)+", " ",
            sub(r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
            lambda mo: ' ' + mo.group(0).lower(), s)).split())

    @staticmethod
    def squash(the_list: list) -> list:
        """[turns a 2d array into a flat one]

        Args:
            the_list ([list]): [a 2d array]

        Returns:
            [list]: [a flattened 1d array]
        """
        return [inner for outer in the_list for inner in outer]

    @staticmethod
    def chunk(list: list, size: int) -> list:
        """ chunk a list into batches """
        return [list[i:i + size] for i in range(0, len(list), size)]

    @staticmethod
    def dictify(arr: list) -> dict:
        """[turns a list into a dictionary where the list items are the keys]

        Args:
            arr ([list]): [list to change]

        Returns:
            [dict]: [a new dict where the list items are now the keys]
        """
        return dict().fromkeys(arr, 0)

    @staticmethod
    def is_empty(some_str: str) -> bool:
        return (not some_str.strip())

    @staticmethod
    def unique(some_arr: list) -> list:
        """[removes duplicates from a list]

        Args:
            some_arr ([list]): [list containing duplicates]

        Returns:
            [list]: [a list containing no duplicates]
        """
        return list(set(some_arr))

    @staticmethod
    def chunks(iterable, size: int, format=iter):
        """ Iterate over any iterable (list, set, file, stream, strings, whatever), of ANY size """
        it = iter(iterable)
        while True:
            yield format(chain((it.next(),), islice(it, size - 1)))
    # >>> l = ["a", "b", "c", "d", "e", "f", "g"]
    # >>> for chunk in chunks(l, 3, tuple):
    # ...         print chunk

    @staticmethod
    def clean(lst: list) -> list:
        """[removes falsy values (False, None, 0 and “”) from a list ]

        Args:
            lst ([list]): [lst to operate on]

        Returns:
            [list]: [a new list with falsy values removed]
        """
        return list(filter(None, lst))

    @staticmethod
    def get_vowels(string: str) -> list:
        """[get a list of vowels from the word]

        Args:
            string ([str]): [the word to check]

        Returns:
            [list]: [a list of vowels]
        """
        return [each for each in string if each in 'aeiou']

    @staticmethod
    def untitle(string: str) -> str:
        """[the opposite of title]

        Args:
            str ([str]): [the string to change]

        Returns:
            [str]: [a string with the first character set to lowercase]
        """
        return string[:1].lower() + string[1:]

    @staticmethod
    def merge_dictionaries(a: dict, b: dict) -> dict:
        """[merges 2 dicts]

        Args:
            a ([dict]): [dict a]
            b ([dict]): [dict b]

        Returns:
            [dict]: [a new dict]
        """
        return {**a, **b}

    @staticmethod
    def to_dictionary(keys: list, values: list) -> dict:
        """[take a list of keys and values and returns a dict]

        Args:
            keys ([list]): [a list of keys]
            values ([list]): [a list of value]

        Returns:
            [dict]: [a dictionary]
        """
        return dict(zip(keys, values))

    @staticmethod
    def most_frequent(lst: list) -> list:
        return max(set(lst), key=lst.count)

    @staticmethod
    def is_anagram(first: str, second: str) -> bool:
        return Counter(first) == Counter(second)

    @staticmethod
    def is_palindrome(word: str) -> bool:
        return word == word[::-1]

    @staticmethod
    def acronym(sentence: str) -> str:
        """[pass a sentence, returns the acronym]

        Args:
            sentence ([str]): [typically 3 words]

        Returns:
            [str]: [a TLA (three letter acronym)]
        """
        text = sentence.split()
        a = ""
        for i in text:
            a = a + str(i[0]).upper()
        return a

    @staticmethod
    def frequency(data):
        """[check the frequency of elements in the data]

        Args:
            data ([type]): [the data to check]

        Returns:
            [dict]: [a dict of elements and their frequency]
        """
        freq = {}
        for elem in data:
            if elem in freq:
                freq[elem] += 1
            else:
                freq[elem] = 1
        return freq

    @staticmethod
    def init_assets(dir: str = 'assets') -> None:
        """[creates an assets directory with nested js/css/img dirs]

        Args:
            dir (str, optional): [default directory name]. Defaults to 'assets'.
        """
        from domonic.terminal import mkdir, touch
        mkdir(f"{dir}")
        mkdir(f"{dir}/js")
        mkdir(f"{dir}/css")
        mkdir(f"{dir}/img")
        touch(f"{dir}/js/master.js")
        touch(f"{dir}/css/style.css")
        return

    @staticmethod
    def url2file(url: str) -> str:
        """[gen a safe filename from a url. by replacing '/' for '_' and ':' for '__' ]

        Args:
            url ([str]): [the url to turn into a filename]

        Returns:
            [str]: [description]
        """
        import urllib
        url = "_".join(url.split("/"))
        url = "__".join(url.split(":"))
        filename = urllib.parse.quote_plus(url, '')
        return filename

    @staticmethod
    def permutations(word: str) -> list:
        """[provides all the possible permutations of a given word]

        Args:
            word ([str]): [the word to get permutations for]

        Returns:
            [list]: [a list of permutations]
        """
        from itertools import permutations
        return [''.join(perm) for perm in list(permutations(word))]

    @staticmethod  # TODO - remove as we have color class. (might be getting used in examples)
    def random_color(self):
        r = lambda: random.randint(0, 255)
        return str('#%02X%02X%02X' % (r(), r(), r()))

    @staticmethod
    def escape(s: str) -> str:
        """[escape a string]

        Args:
            s ([str]): [the string to escape]

        Returns:
            [str]: [the escaped string]
        """
        chars = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&apos;",
            ">": "&gt;",
            "<": "&lt;"
        }
        return "".join(chars.get(c, c) for c in s)

    @staticmethod
    def unescape(s: str) -> str:
        """[unescape a string]

        Args:
            s ([str]): [the string to unescape]

        Returns:
            [str]: [the unescaped string]
        """
        s = s.replace("&lt;", "<")
        s = s.replace("&gt;", ">")
        s = s.replace("&quot;", '"')
        s = s.replace("&apos;", "'")
        s = s.replace("&amp;", "&")
        return s

    @staticmethod
    def replace_between(content: str, match: str, replacement: str, start: int = 0, end: int = 0):
        """[replace some text but only between certain indexes]

        Args:
            content (str): [the content whos text you will be replacing]
            match (str): [the string to find]
            replacement (str): [the string to replace it with]
            start (int, optional): [start index]. Defaults to 0.
            end (int, optional): [end index]. Defaults to 0.

        Returns:
            [str]: [the new string]
        """
        front = content[0:start]
        mid = content[start:end]
        end = content[end:len(content)]
        mid = mid.replace(match, replacement)
        return front + mid + end

    @staticmethod
    def truncate(text: str = '', length: int = 0) -> str:
        """[truncates a string and appends 3 dots]

        Args:
            text (str, optional): [the text to truncate]. Defaults to ''.
            length (int, optional): [the max length]. Defaults to 0.

        Returns:
            [str]: [the truncated string]
        """
        if len(text) > length:
            return text[0:length] + "..."
        else:
            return text + "..."

    @staticmethod
    def digits(text: str = '') -> str:
        """[takes a string of mix of digits and letters and returns a string of digits]

        Args:
            text (str, optional): [the text to change]. Defaults to ''.

        Returns:
            [str]: [a string of digits]
        """
        if isinstance(text, int):
            return str(text)
        elif isinstance(text, float):
            return str(int(text))
        elif isinstance(text, str):
            return ''.join(i for i in text if i.isdigit())
        else:
            try:
                return str(text)
            except Exception:
                raise ValueError("text must be a string")

    @staticmethod
    def has_internet(url: str = 'http://www.google.com/', timeout: int = 5) -> bool:
        """[check if you have internet connection]

        Args:
            url (str, optional): [the url to check]. Defaults to 'http://www.google.com/'.
            timeout (int, optional): [the timeout]. Defaults to 5.

        Returns:
            [bool]: [True if you have internet]
        """
        import requests
        try:
            _ = requests.head(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            # print("No internet connection available.")
            return False

    @staticmethod
    def is_nix() -> bool:
        """[check if the system is a nix based system]

        Returns:
            [bool]: [True if it is a nix based system]
        """
        import os
        return os.name == "posix"

    @staticmethod
    def is_mac() -> bool:
        """[check if the system is a mac]

        Returns:
            [bool]: [True if the system is a mac]
        """
        import sys
        return sys.platform == "darwin"

    @staticmethod
    def is_windows() -> bool:
        """[check if the system is a windows]

        Returns:
            [bool]: [True if windows]
        """
        import os
        return os.name == "nt"

    @staticmethod
    def is_linux() -> bool:
        """[check if the system is a linux]

        Returns:
            [bool]: [description]
        """
        import sys
        return sys.platform.startswith('linux')

    # def convert_file(filepath, filetype=None):
    #     """
    #         convert a file to a different file type
    #         mostly deals with config files
    #     """
    #  files = ['json', 'ini', 'xml', 'yaml', 'yml', 'toml', 'properties', 'conf', 'rc', 'sh', 'bash', 'bat', 'cmd', 'c', 'cpp', 'h', 'hpp', 'java', 'js', 'json', 'md', 'markdown', 'pl', 'py', 'rb', 'sh', 'sql', 'txt', 'xml', 'yaml', 'yml', 'toml']

    '''
    @staticmethod
    def yeahnah(x):
        """ returns a boolean for any given user reply
        """
        reply = x.lower()
        if reply.lower() in ['yeah', "y", "yes", "yup", "si", "yep", "yeah", "yep"]:
            return True
        elif reply.lower() in ['nah', "no", "nope", "n"]:
            return False
        else:
            # return a probability between 0 and 1 for either yes or no based on which list has the most similar words to the input
            # return max([float(reply.count(x)) / len(reply) for x in ['yeah', "y", "yes", "yup", "si", "yep", "yeah", "yep"]]) > max([float(reply.count(x)) / len(reply) for x in ['nah', "n", "no", "nope", "nop", "nope", "n", "nope"]])
            # return max([float(reply.count(x)) / len(reply) for x in ['yeah', "y", "yes", "yup", "si", "yep", "yeah", "yep"]]) > 0.5
        else:
            return None
    '''

    # def get_ip(self):
    #     """[get the current ip]

    #     Returns:
    #         [str]: [the current ip]
    #     """
    #     import socket
    #     return socket.gethostbyname(socket.gethostname())

    # def get_hostname(self):
    #     """[get the current hostname]

    #     Returns:
    #         [str]: [the current hostname]
    #     """
    #     import socket
    #     return socket.gethostname()

    # def get_mac(self):
    #     """[get the current mac]

    #     Returns:
    #         [str]: [the current mac]
    #     """
    #     import uuid
    #     return uuid.UUID(int=uuid.getnode()).hex[-12:]

    # def get_ip_mac(self):
    #     """[get the current ip and mac]

    #     Returns:
    #         [str]: [the current ip and mac]
    #     """
    #     return self.get_ip() + "|" + self.get_mac()

    # def get_os(self):
    #     """[get the current os]

    #     Returns:
    #         [str]: [the current os]
    #     """
    #     import platform
    #     return platform.system()

    # def get_os_version(self):
    #     """[get the current os version]

    #     Returns:
    #         [str]: [the current os version]
    #     """
    #     import platform
    #     return platform.release()

    # def get_os_arch(self):
    #     """[get the current os architecture]

    #     Returns:
    #         [str]: [the current os architecture]
    #     """
    #     import platform
    #     return platform.machine()

    # def get_cpu(self):
    #     """[get the current cpu]

    #     Returns:
    #         [str]: [the current cpu]
    #     """
    #     import platform
    #     return platform.processor()

    @staticmethod
    def numberToBase(n, b):
        if n == 0:
            return [0]
        digits = []
        while n:
            digits.append(int(n % b))
            n //= b
        return digits[::-1]
