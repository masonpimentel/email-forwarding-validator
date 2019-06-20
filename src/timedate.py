from lib.messages import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("msg")
args = parser.parse_args()

print_message(args.msg, "CRONJOB", "verbose")
