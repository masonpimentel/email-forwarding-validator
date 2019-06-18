import json
import os


def config_get_dev():
    with open("../dev_config.json") as config_file:
        return json.load(config_file)


def config_get_user():
    with open("../user_config.json") as config_file:
        return json.load(config_file)


def config_get_backup_size():
    return config_get_user()["backup_size"]


def config_get_email_cycle_delay():
    return config_get_user()["email_cycle_delay"]


def config_get_num_cycle():
    return config_get_user()["num_cycle"]


def config_get_receiver_email():
    return config_get_user()["receiver"]["test"]


def config_get_receiver_info_email():
    return config_get_user()["receiver"]["info"]


def config_get_sender_gmail():
    return config_get_user()["sender_gmail"]


def config_get_message_bodies():
    return config_get_dev()["message_body"]


def config_get_repo_path():
    return config_get_dev()["paths"]["repo_path"]


def config_get_python_invoker():
    return config_get_dev()["python_invoker"]


def config_get_scopes():
    return config_get_dev()["scopes"]


def config_get_subjects():
    return config_get_dev()["subject"]


def config_get_verbosities():
    return config_get_dev()["verbosity"]


def config_replace_cronjob_line(find_string, replace_string_with, contains=False):
    f = open("../cronjob", "r")
    lines = f.readlines()
    f.close()

    for i, line in enumerate(lines):
        if (contains and find_string in line) or (line.rstrip("\n") == find_string):
            lines[i] = replace_string_with + "\n"
            f = open("../cronjob", "w")
            contents = "".join(lines)
            f.write(contents)
            f.close()
            return True

    return False


def config_clear_user_config():
    user_config = config_get_user()
    user_config["receiver"]["test"] = "fill_this_in"
    user_config["receiver"]["info"] = "fill_this_in"
    user_config["sender_gmail"] = "fill_this_in"
    with open("../user_config.json", "w") as config_file:
        json.dump(user_config, config_file, indent=4, sort_keys=True)


def config_clear_receive_credentials():
    new_config = {}
    new_config["@note"] = "add receive credentials here"
    with open("../receive/credentials-receive.json", "w") as config_file:
        json.dump(new_config, config_file, indent=4, sort_keys=True)


def config_clear_send_credentials():
    new_config = {}
    new_config["@note"] = "add send credentials here"
    with open("../send/credentials-send.json", "w") as config_file:
        json.dump(new_config, config_file, indent=4, sort_keys=True)


def config_clear_cronjob_repo_path():
    config_replace_cronjob_line("repo_path=", "{repo_path_cmd}", True)


def config_delete_tokens():
    os.remove("../receive/token.json")
    os.remove("../send/token.json")
