import json

def presence_mess(account_name, time_connect):
    mess = {
        "action": "presence",
        "time": time_connect,
        "type": "status",
        "user": {
            "account_name": account_name,
            "status": "i am connect!"
        }
    }
    return json.dumps(mess)


def quit_mess():
    mess = {
        "action": "quit"
    }
    return json.dumps(mess)