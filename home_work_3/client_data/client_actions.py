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


def join_mess(time, room_name):
    mess = {
        "action": "join",
        "time": time,
        "room": room_name,
    }
    return json.dumps(mess)


def message(time, to_name: str, from_name: str, message: str, is_room=True):
    if is_room:
        to_name = '#'+to_name

    mess = {
        "action": "msg",
        "time": time,
        "to": to_name,
        "from": from_name,
        "message": message,
    }
    return json.dumps(mess)


def quit_mess():
    mess = {
        "action": "quit"
    }
    return json.dumps(mess)
