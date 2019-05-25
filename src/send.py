from lib.messages import *
from lib.debugging import *
import time
import json

with open("../config.json") as config_file:
    json_config = json.load(config_file)
    EMAIL_CYCLE_DELAY = json_config["email_cycle_delay"]
    HALF_EMAIL_CYCLE_DELAY = EMAIL_CYCLE_DELAY/2
    EMAIL_CYCLES = json_config["num_cycle"]


def main():
    service = get_service('../send/token.json')
    message = create_message()

    for i in range(0, EMAIL_CYCLES):
        print_message("Sending message " + str(i + 1), "SEND", "verbose")
        send_message(service, message, "SEND")
        time.sleep(EMAIL_CYCLE_DELAY)

    print_message("Waiting half a cycle to synchronize with receive offset", "SEND", "verbose")
    time.sleep(HALF_EMAIL_CYCLE_DELAY)

if __name__ == '__main__':
    main()

