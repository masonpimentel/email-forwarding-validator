from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import argparse
import json

with open("../config.json") as config_file:
    json_config = json.load(config_file)
    RECEIVE_SCOPES = json_config["scopes"]["receive"]
    SEND_SCOPES = json_config["scopes"]["send"]


def create_token(token_path, credentials_path, scopes):
    store = file.Storage(token_path)
    creds = store.get()
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credentials_path, scopes)
        flags = parser.parse_args()
        creds = tools.run_flow(flow, store, flags)
        build('gmail', 'v1', http=creds.authorize(Http()))
        return True
    else:
        return False


def main():
    res = create_token("../send/token.json", "../send/credentials-send.json", SEND_SCOPES)
    if not res:
        print("Token for send already exists!")
    res = create_token("../receive/token.json", "../receive/credentials-receive.json", RECEIVE_SCOPES)
    if not res:
        print("Token for receive already exists!")


if __name__ == '__main__':
    main()
