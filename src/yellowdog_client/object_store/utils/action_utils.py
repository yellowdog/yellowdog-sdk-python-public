from typing import Callable
import sys


class ActionUtils(object):
    @staticmethod
    def always_execute_both(action1: Callable, action2: Callable) -> None:
        exceptions = []

        # noinspection PyBroadException
        try:
            action1()
        except Exception:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            exceptions.append((ex_type, ex_value, ex_traceback))

        # noinspection PyBroadException
        try:
            action2()
        except Exception:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            exceptions.append((ex_type, ex_value, ex_traceback))

        if len(exceptions) == 0:
            return
        elif len(exceptions) == 1:
            raise exceptions[0][1]
        else:
            raise Exception(". ".join([str(error[1]) for error in exceptions])) from exceptions[0][2]
