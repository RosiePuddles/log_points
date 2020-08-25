from inspect import getframeinfo, stack
import os
import signal


outputLog = True
logNumber = {}
max_logs_per_line = 100


def max_log(maximum_log_points_per_line):
    global max_logs_per_line
    max_logs_per_line = maximum_log_points_per_line


def kill(pid):
    os.kill(pid, signal.SIGKILL)


def log_point(message=None, pointer_=False):
    global outputLog
    global logNumber
    line_number = getframeinfo(stack()[2][0]).lineno
    if line_number not in logNumber:
        logNumber[line_number] = 0
    logNumber[line_number] += 1
    if logNumber[line_number] > max_logs_per_line:
        kill(os.getpid())
    if outputLog:
        caller = getframeinfo(stack()[2][0])
        out = f'{{{caller.filename}}} Log : {caller.lineno}'
        if message is not None: out += f' - {message}'
    if pointer_:
        return out
    else:
        print(out)
    logNumber[line_number] += 1


def pointer(message=None, back_colour=0, text_colour=0):
    text_colour += 1 if text_colour == back_colour else 0
    formatted_message = f'\x1b[0;{30 + (text_colour % 8)};{40 + (back_colour % 8)}m{log_point(message, True)}\x1b[0m'
    print(formatted_message)
