from flask import Flask, request
import RPi.GPIO as GPIO
import time
from fb import Facebook_messages
from terminal import Terminal

#Raspberry Pi
COLORS = ("green", "red")
LEDS = {COLORS[0]: 16, COLORS[1]: 18}

#Set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LEDS[COLORS[0]], GPIO.OUT)
GPIO.setup(LEDS[COLORS[1]], GPIO.OUT)

term = Terminal()
fb = Facebook_messages()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def subscription():
    # when the endpoint is registered as a webhook, it must
    # return the 'hub.challenge' value in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == SUBSCRIPTION_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webook():

    data = request.get_json()
    fb.log(data)  # you may not want to fb.log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID

                if messaging_event.get("message"):  # someone sent us a message
                    message_text = messaging_event["message"]["text"]  # the message's text
                    if message_text == "menu" and term.term_started == False:
                        fb.send_message_msg(sender_id, "You're now in the main menu:")
                    elif message_text == "term" and term.term_started == False:
                        term.start_terminal()
                        response = term.execute_command("pwd")
                        fb.simple_msg(sender_id, "Terminal mode started at: " + response)
                    elif message_text == "term" and term.term_started == True:
                        fb.simple_msg(sender_id, "Terminal already running")
                    elif message_text != "term" and message_text != "menu" and term.term_started == True:
                        response = term.execute_command(message_text)
                        fb.simple_msg(sender_id, response)

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    color = messaging_event["postback"]["payload"]

                    GPIO.output(LEDS[color], not GPIO.input(LEDS[color]))

                    fb.send_message_msg(sender_id, "This is a response to postback: " + str(GPIO.input(LEDS[color])))

    return "ok", 200



#Cut the response into 320 char messages



if __name__ == '__main__':
    app.run()
