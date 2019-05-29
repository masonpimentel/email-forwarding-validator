from lib.utils import *
import time


def format_type(padding, body):
    s = " [" + body + "]"
    return s.ljust(padding, " ")


def format_prefix(padding, body):
    s = body + ":"
    return s.ljust(padding, " ")


def print_message(message, type_prefix, message_type):
    if message_type == "info":
        print(str(time.strftime("%c")) + format_type(12, "INFO") + format_prefix(12, type_prefix) + message)
    elif message_type == "message":
        print(str(time.strftime("%c")) + format_type(12, "MESSAGE") + format_prefix(12, type_prefix) + message)
    elif message_type == "error":
        print(str(time.strftime("%c")) + format_type(12, "ERROR") + format_prefix(12, type_prefix) + message)
    elif message_type == "debug":
        if config_get_verbosities()["debug"]:
            print(str(time.strftime("%c")) + format_type(12, "DEBUG") + format_prefix(12, type_prefix) + message)
    elif message_type == "verbose":
        if config_get_verbosities()["verbose"]:
            print(str(time.strftime("%c")) + format_type(12, "VERBOSE") + format_prefix(12, type_prefix) + message)
    else:
        print(str(time.strftime("%c")) + format_type(12, "ERROR") + format_prefix(12, type_prefix) + "Unknown type argument supplied to print_message")

