from apiclient import errors
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from email.message import EmailMessage
import base64
import time

from lib.debugging import *
from lib.utils import *


def get_service(token_path):
    store = file.Storage(token_path)
    creds = store.get()
    if not creds or creds.invalid:
        return None
    else:
        return build('gmail', 'v1', http=creds.authorize(Http()))


def format_info_message_body(expected_count, actual_count):
    s = config_get_message_bodies()["info"].replace("{0}", str(actual_count))
    s = s.replace("{1}", str(expected_count))
    return s


def format_test_message_body():
    epoch = str(int(time.time()))
    return config_get_message_bodies()["test"].replace("{0}", epoch)


def create_message(info=False, expected_count=None, actual_count=None):
    msg = EmailMessage()
    if info:
        msg['To'] = config_get_receiver_info_email()
        msg['Subject'] = config_get_subjects()["info"]
        msg.set_content(format_info_message_body(expected_count, actual_count))
    else:
        msg['To'] = config_get_receiver_email()
        msg['Subject'] = config_get_subjects()["test"]
        msg.set_content(format_test_message_body())
    msg['From'] = config_get_sender_gmail()

    return {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode()}


def send_message(service, message, type_prefix):
    try:
        message = (service.users().messages().send(userId='me', body=message).execute())
        print_message("Sending message ID: {id}".format(id=message['id']), type_prefix, "verbose")
        return message
    except errors.HttpError as e:
        print_message("An error occurred: {error}".format(error=e), type_prefix, "error")
        print_message("Please check the email addresses entered in user_config.json", type_prefix, "error")
        raise e
