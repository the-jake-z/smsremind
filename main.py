from flask import Flask, request, redirect
from mongoengine import *
from config import *
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.config.from_object(os.environ.get('CONFIG_CLASS', 'config.DevelopmentConfig'))

connect(host=app.config['MONGODB_SETTINGS']['host'] or None)

def Lists(Document):
    subs = ListField(StringField())
    items = ListField(StringField())


def create_list(full_message):
    pass


def delete_list(full_message):
    pass


def add_item(full_message):
    pass


def remove_item(full_message):
    pass


def add_sub(full_message):
    pass


def remove_sub(full_message):
    pass


def stop(full_message):
    pass


def help(full_message):
    pass

commands = {
    'create': create_list,
    'delete': delete_list,
    'add': add_item,
    'rm': remove_item,
    'sub': add_sub,
    'unsub': remove_sub,
    'stop': stop,
    'help': help
}


def build_reply(message):
    resp = MessagingResponse()
    resp.message(message)
    return str(resp)


@app.route('/', methods=['GET', 'POST'])
def listener():
    return build_reply("Greetings from SMSRemind")

if __name__ == '__main__':
    debug = not app.config['CONFIGURATION'] == "PRODUCTION"
    app.run(debug=debug, port=app.config['PORT'], host="0.0.0.0")
