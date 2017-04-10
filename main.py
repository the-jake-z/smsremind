from flask import Flask, request, redirect
from mongoengine import *
from config import *
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.config.from_object(os.environ.get('CONFIG_CLASS', 'config.DevelopmentConfig'))

connect(host=app.config['MONGODB_SETTINGS']['host'] or None)


class Lists(Document):
    subs = ListField(StringField())
    items = ListField(StringField())
    name = StringField()


def create_list(from_number, full_message):
    cmd, name = full_message.split(' ')
    l = Lists(subs=[from_number], items=[], name=name).save()
    return 'list \"{name}\" created'.format(name=name)


def delete_list(from_number, full_message):
    cmd, name = full_message.split(' ')
    l = Lists.objects(subs=[from_number], name=name).first()
    l.delete()
    return 'list \"{name}\" deleted'.format(name=name)


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


def help_message(from_number, full_message):
    return r"""
    SMSRemind
    commons ops:
    create [list]
    delete [list]
    add [list] [item]
    rm [list] [item index]
    sub [list] [phone]
    unsub [list] [phone]
    subs
    stop
    """

commands = {
    'create': create_list,
    'delete': delete_list,
    'add': add_item,
    'rm': remove_item,
    'sub': add_sub,
    'unsub': remove_sub,
    'stop': stop,
    'help': help_message
}


def build_reply(message):
    resp = MessagingResponse()
    resp.message(message)
    return str(resp)


@app.route('/', methods=['GET', 'POST'])
def listener():
    return build_reply(commands['help'](request.values.get('From', None), ''))

if __name__ == '__main__':
    debug = not app.config['CONFIGURATION'] == "PRODUCTION"
    app.run(debug=debug, port=app.config['PORT'], host="0.0.0.0")
