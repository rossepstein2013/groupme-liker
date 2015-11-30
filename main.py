"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
import urllib2, json
from flask import Flask, request, Response, redirect
from google.appengine.ext import ndb
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

GROUPME_BASE_URL = "https://api.groupme.com/v3"
SENDER_ID = "2333940"
GROUP_ID = "1683521"

class AccessToken(ndb.Model):
    access_token = ndb.StringProperty()
    user_name = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_tokens(cls):
        return cls.query().order(-cls.date)

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    tokens = AccessToken.query_tokens().fetch(100)
    output_string = "Go <a href=\"https://oauth.groupme.com/oauth/authorize?client_id=VQWMfHmrv6gRIDUWdFSBWOkPuV5ruNBYw6tmvusL0JKugwWs\">here<a/> to authenticate<br/><br/>Users who have authenticated:<br/>"
    for token in tokens:
        output_string += token.user_name + "<br/>"
    return output_string

@app.route('/callback')
def callback():
    access_token = request.args.get('access_token')
    name = get_name_from_token(access_token)
    access_token = AccessToken(access_token = access_token, user_name = name)

    access_token.put()
    return "Got it, " + name

@app.route('/webhook/',methods=['POST'])
def webhook():
    data = json.loads(request.data)
    if data['sender_id'] == SENDER_ID:
        make_all_users_like_message(data['id'])

    return "test response"

def make_all_users_like_message(message_id):
    tokens = AccessToken.query_tokens().fetch(100)
    for token in tokens:
        post_url = GROUPME_BASE_URL + "/messages/" + GROUP_ID + "/" + message_id + "/like?token=" + token.access_token
        response = urllib2.urlopen(post_url, {})

    return True


def get_name_from_token(access_token):
    response = urllib2.urlopen(GROUPME_BASE_URL + "/users/me?token=" + access_token)
    data = json.load(response)
    name = data['response']['name']
    return name


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

if __name__ == '__main__':
    app.run()