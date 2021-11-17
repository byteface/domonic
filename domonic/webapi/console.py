"""
    domonic.webapi.console
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/Console_API
"""


class Console(object):

    @staticmethod
    def log(msg: str, substitute=None, *args):  # -> None:
        """prints a message to the console

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
    def count() -> int:
        """returns the number of times count() has been called"""
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

    @staticmethod
    def clear():
        """clear

        clears the console
        """
        print("\033[2J")

    # @staticmethod
    # def dir(obj): # TODO - does this exist?
    #     """dir

    #     prints the properties of an object
    #     """
    #     print(dir(obj))

    # @staticmethod
    # def dirxml(obj): # TODO - does this exist?
    #     """dirxml

    #     prints the properties of an object
    #     """
    #     print(dir(obj))

    # @staticmethod
    # def group(msg: str):
    #     """group

    #     prints a message to the console
    #     """
    #     print(msg)

    # @staticmethod
    # def groupCollapsed(msg: str):
    #     """groupCollapsed

    #     prints a message to the console
    #     """
    #     print(msg)

    # @staticmethod
    # def groupEnd():
    #     """groupEnd

    #     prints a message to the console
    #     """
    #     print("")

    # @staticmethod
    # def profile(label: str):
    #     """[starts a profiler]

    #     Args:
    #         label (str): [The name to give the new profiler.]
    #     """
    #     pass

    # @staticmethod
    # def profileEnd(label: str):
    #     """[stops a profiler]

    #     Args:
    #         label (str): [The name to of the profiler to stop]

    #     Returns:
    #         [type]: [label: time - profiler ended]
    #     """
    #     pass

    @staticmethod
    def table(data: list):
        """table

        prints a table to the console
        """
        print(data)

    # @staticmethod
    # def timeStamp(label: str):
    #     """[starts a timer]

    #     Args:
    #         label (str): [The name to give the new timer.]
    #     """
    #     Console._timers[label] = Console._getTime()

    def __init__(self, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        # group()
        # groupCollapsed()
        # groupEnd()
        # def table(json_str, filter_array):
        # trace()
        Console.__count_var = 0


Console.info = Console.log  # info()
Console.warn = Console.log  # warn()
console = Console
