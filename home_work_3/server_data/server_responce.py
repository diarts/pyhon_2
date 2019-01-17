import json

def accept_presence():
    mess = {
        "responce": 202,
        "alert": "connecting to server is successful"
    }
    return json.dumps(mess)

def accept_required(room):
    mess = {
        "responce": 225,
        "alert": f"connecting to room {room} is successful"
    }
    return json.dumps(mess)

def wrong_request():
    mess = {
        "responce": 400,
        "error": "You request not compliant"
    }
    return json.dumps(mess)


def client_alredy_connected():
    mess = {
        "responce": 409,
        "error": "You already connected on server"
    }
    return json.dumps(mess)