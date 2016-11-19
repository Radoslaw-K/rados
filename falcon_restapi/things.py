# Let's get this party started!
import falcon
import json

LEDS = {"red": "RED COLOR", "green": "GREEN COLOR"}

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class LedsResource(object):
        def on_get(self, req, resp):
            """Handles GET requests"""
            resp.status = falcon.HTTP_200  # This is the default status

            resp.set_header('Powered-By', 'Falcon')
            resp.body = (json.dumps({"led_url": req.url + "led/{green | red}/"
                                    ,"led_url_POST": {"state": "{1 | 0}"}}))

class LedsResourceTwo(object):
        def on_get(self, req, resp, color):
            """Handles GET requests"""
            resp.status = falcon.HTTP_200  # This is the default status

            resp.set_header('Powered-By', 'Falcon')
            resp.body = ("hello world " + str(LEDS.get(color)))

        def on_post(self, req, resp, color):
            print "received color:",color,"result:", str(LEDS.get(color))

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
leds = LedsResource()
leds_two = LedsResourceTwo()

# things will handle all requests to the '/things' URL path
app.add_route('/', leds)
app.add_route('/led/{color}', leds_two)


if __name__ == "__main__":
    pass
