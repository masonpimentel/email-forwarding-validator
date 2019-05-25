from apiclient import errors
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from email.message import EmailMessage
from lib.debugging import *
import base64
import argparse
import json

with open("../config.json") as config_file:
    json_config = json.load(config_file)
    VERBOSE = json_config["verbosity"]["verbose"]
    SENDER_GMAIL = json_config["sender_gmail"]
    RECEIVER_EMAIL = json_config["receiver"]["test"]
    MESSAGE_SUBJECT = json_config["subject"]["test"]
    MESSAGE_BODY = json_config["message_body"]["test"]
    INFO_RECEIVER_EMAIL = json_config["receiver"]["info"]
    INFO_MESSAGE_SUBJECT = json_config["subject"]["info"]
    INFO_MESSAGE_BODY = json_config["message_body"]["info"]
    RECEIVE_SCOPES = json_config["scopes"]["receive"]
    SEND_SCOPES = json_config["scopes"]["send"]


def get_service(token_path):
    store = file.Storage(token_path)
    creds = store.get()
    if not creds or creds.invalid:
        return None
    else:
        return build('gmail', 'v1', http=creds.authorize(Http()))


def format_info_message_body(expected_count, actual_count):
    s = INFO_MESSAGE_BODY.replace("{0}", str(actual_count))
    s = s.replace("{1}", str(expected_count))
    return s


def create_message(info=False, expected_count=None, actual_count=None):
    msg = EmailMessage()
    if info:
        msg['To'] = INFO_RECEIVER_EMAIL
        msg['Subject'] = INFO_MESSAGE_SUBJECT
        msg.set_content(format_info_message_body(expected_count, actual_count))
    else:
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = MESSAGE_SUBJECT
        msg.set_content(MESSAGE_BODY)
    msg['From'] = SENDER_GMAIL

    return {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode()}


def send_message(service, message, type_prefix):
    try:
        message = (service.users().messages().send(userId='me', body=message).execute())
        print_message("Sending message ID: {id}".format(id=message['id']), type_prefix, "verbose")
        return message
    except errors.HttpError as e:
        print_message("An error occurred: {error}".format(error=e), type_prefix, "error")
