from flask import Flask, request, redirect
from mongoengine import *
from config import *

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

@app.route('/', methods=['GET','POST'])
def listener():
    print("hello, world")
    return "success"

if __name__ == '__main__':
    app.run(debug=True)
