"""
    domonic.webapi.console
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/Console_API
"""


class Console(object):  # TODO - test - migrated here from the DOM

    @staticmethod
    def log(msg: str, substitute=None, *args):
        """log

        prints a message to the console

        Args:
            msg (str): msg to log
            substitute : replaces %s or %d with this
        """
        msg = str(msg)
        argstring = str(*args)
        if substitute is not None:
            if '%d' not in msg and '%s' not in msg:
                argstring = argstring + " " + str(substitute)
            elif isinstance(substitute, (int, float)):
                msg = str(substitute).join(msg.split('%d'))
            elif isinstance(substitute, str):
                msg = substitute.join(msg.split('%s'))

        # print(args)
        print(msg + argstring)
        return msg + argstring

    __count_var = 0

    @staticmethod
    def count():
        """count

        increments a number
        """
        Console.__count_var = Console.__count_var + 1
        return Console.__count_var

    @staticmethod
    def error(error):
        """error

        """
        raise error

    _timers = {}

    @staticmethod
    def _getTime():
        import time
        try:
            return time.time_ns() // 1000
        except Exception:
            # python 3.6 doesn't have _ns
            return time.time() * 1000000

    @staticmethod
    def time(label: str):
        """[starts a timer]

        Args:
            label (str): [The name to give the new timer.]
        """
        Console._timers[label] = Console._getTime()  # time.time_ns() // 1000

    @staticmethod
    def timeLog(label: str = None):
        """[summary]

        Args:
            label (str): [The name to of the timer to log]

        Returns:
            [type]: [description]
        """
        try:
            # if label = None
            end = Console._getTime()  # time.time_ns() // 1000
            print(str(end - Console._timers[label]) + "ms")
            return str(end - Console._timers[label]) + "ms"
        except Exception:
            print('Timer ' + label + ' does not exist')

    @staticmethod
    def timeEnd(label: str):
        """[stops a timer]

        Args:
            label (str): [The name to of the timer to stop]

        Returns:
            [type]: [label: time - timer ended]
        """
        try:
            end = Console._getTime()  # time.time_ns() // 1000
            fin = end - Console._timers[label]
            del Console._timers[label]
            print(str(label) + ": " + str(fin) + "ms - timer ended")
            return str(label) + ": " + str(fin) + "ms - timer ended"
        except Exception:
            print('Timer ' + label + ' does not exist')

    @staticmethod
    def assert_(assertion: bool, msg: str = None):
        """[return an error message if the assertion is false. If the assertion is true, nothing happens.]

        Args:
            assertion (bool): [any boolean expression]
            msg (str): [output if expression if false]
        """
        if not assertion:
            print(msg)
            return msg

    def __init__(self, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        # self.log = lambda msg : print(msg)
        # clear()
        # group()
        # groupCollapsed()
        # groupEnd()
        # info()
        # def table(json_str, filter_array):
        # trace()
        # warn()
        __count_var = 0


Console.info = Console.log
Console.warn = Console.log
console = Console
