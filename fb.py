import os
import sys
import json
import requests

SUBSCRIPTION_TOKEN = "subscription_token_737c677d"
ACCESS_TOKEN = "EAAEwaZC3yaowBADNvIurTHjlrN4PZAG200pkqtl0zlejUps3tc1fuukwjr4WR68wMlhZBvoIbikd1CT1SR6vejwyrMqH9IO8TYMCWZCYFmsXe8XAl7ZBiMXLWbbNZBBjNcQKq9QPZBCGOD4MWHWJ7qrHTHrorU5aD0N2aKNfeiEOV0LkDoZAXzz4"
GRAPH_API = "https://graph.facebook.com/v2.6/me/messages"


class Facebook_messages():

    def __init__(self):
        pass

    def simple_msg(self, recipient_id, message_text):

        self.log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

        params = {"access_token": ACCESS_TOKEN}
        headers = {"Content-Type": "application/json"}
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
            })

        r = requests.post(GRAPH_API, params=params, headers=headers, data=data)
        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)

    def send_message(self, recipient_id, message_text):

        self.log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

        params = {"access_token": ACCESS_TOKEN}
        headers = {"Content-Type": "application/json"}
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
    #            "text": message_text
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": message_text,
                        "buttons": [{
                            "type": "postback",
                            "title": "Toggle " + COLORS[0] + " LED",
                            "payload": COLORS[0]
                        },
                        {
                            "type": "postback",
                            "title": "Toggle " + COLORS[1] + " LED",
                            "payload": COLORS[1]
                        }]
                    }
                }
            }
        })

        r = requests.post(GRAPH_API, params=params, headers=headers, data=data)
        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)


    def log(self, message):  # simple wrapper for logging to stdout on heroku
        print str(message)
        sys.stdout.flush()
