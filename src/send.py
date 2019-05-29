from lib.messages import *
from lib.debugging import *
from lib.utils import *

import time
import json


def main():
    service = get_service('../send/token.json')
    message = create_message()

    for i in range(0, config_get_num_cycle()):
        print_message("Sending message " + str(i + 1), "SEND", "verbose")
        send_message(service, message, "SEND")
        time.sleep(config_get_email_cycle_delay())

    print_message("Waiting half a cycle to synchronize with receive offset", "SEND", "verbose")
    time.sleep(config_get_email_cycle_delay()/2)

if __name__ == '__main__':
    main()

