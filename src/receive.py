from lib.messages import *
from lib.debugging import *
from lib.utils import *

import time


def get_messages(service, clearing):
    max_num = config_get_backup_size() + (config_get_num_cycle() * 2)

    if clearing:
        print_message("Getting messages for inbox clearing...", "RECEIVE", "verbose")
    else:
        print_message("Getting messages for initial count...", "RECEIVE", "verbose")
    msg_object = service.users().messages().list(userId='me', q='from:' + config_get_sender_gmail() + ' subject:"' + config_get_subjects()["test"] + '"', maxResults=max_num).execute()

    if "messages" in msg_object:
        return msg_object['messages']
    else:
        return None


def clear_inbox(service):
    msgs = get_messages(service, True)
    if not msgs:
        return
    else:
        sorted_msgs = get_msg_data_sorted(service, msgs)
        trash_amt = len(sorted_msgs) - config_get_backup_size()
        print_message("Clearing inbox to backup size: " + str(config_get_backup_size()) + ", deleting " + str(trash_amt) + " message(s)", "RECEIVE", "verbose")
        for i in range(0, trash_amt):
            service.users().messages().trash(userId='me', id=sorted_msgs[i][0]).execute()


# returns all the messages in tuples of (<message id>, <timestamp epoch>)
# sorted newest to oldest
def get_msg_data_sorted(service, messages):
    msg_data = []

    for m in messages:
        msg_id = m['id']
        data = service.users().messages().get(userId='me', id=msg_id, format='minimal').execute()
        msg_data.append((msg_id, int(data['internalDate'])))

    return sorted(msg_data, key=lambda date: date[1])


def get_count(service, clearing):
    msgs = get_messages(service, clearing)
    if not msgs:
        return 0
    else:
        return len(msgs)


def main():
    service = get_service('../receive/token.json')
    print_message("Waiting half an email cycle...", "RECEIVE", "verbose")
    time.sleep(config_get_email_cycle_delay()/2)

    init_count = get_count(service, False)
    delay = config_get_email_cycle_delay() * config_get_num_cycle()
    print_message("Initial count: " + str(init_count) + ", waiting " + str(delay) + " seconds...", "RECEIVE", "verbose")

    time.sleep(delay)

    new_count = get_count(service, True)
    diff = new_count - init_count
    # account for the first one already being in inbox at init_count
    expected_messages = config_get_num_cycle() - 1
    if diff != expected_messages:
        print_message("Got a diff of " + str(diff) + ", expected " + str(expected_messages), "RECEIVE", "error")
        send_message(get_service('../receive/token.json'), create_message(True, expected_messages, diff), "RECEIVE")
    else:
        print_message("All good!", "RECEIVE", "message")

    clear_inbox(service)


if __name__ == '__main__':
    main()

