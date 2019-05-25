from lib.messages import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("val")
args = parser.parse_args()

if args.val == "1":
    print_message("send.py not running", "CRONJOB", "verbose")
elif args.val == "2":
    print_message("receive.py not running", "CRONJOB", "verbose")
elif args.val == "3":
    print_message("Re-running send and receive", "CRONJOB", "verbose")
elif args.val == "4":
    print_message("Still running", "CRONJOB", "verbose")
