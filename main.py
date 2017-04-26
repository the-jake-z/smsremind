from flask import Flask, request, redirect
from mongoengine import *
from config import *
from twilio.twiml.messaging_response import MessagingResponse
import phonenumbers

app = Flask(__name__)
app.config.from_object(os.environ.get('CONFIG_CLASS', 'config.DevelopmentConfig'))

connect(host=app.config['MONGODB_SETTINGS']['host'] or None)


class Lists(Document):
    subs = ListField(StringField())
    items = ListField(StringField())
    name = StringField()


def get_user_list(from_number, list_name):
    return Lists(subs=from_number, name=list_name.lower()).first()


def show_lists(from_number, full_message):
    l = Lists.objects(subs=from_number)
    length = l.count() if l else 0
    return '\n'.join('{0}. {1}'.format(i + 1, l[i].name) for i in range(length)) if length > 0 else 'no lists'


def create_list(from_number, full_message):
    cmd, name = full_message.split(' ')
    Lists(subs=from_number, items=[], name=name).save()
    return 'list \"{name}\" created'.format(name=name)


def delete_list(from_number, full_message):
    cmd, name = full_message.split(' ')
    l = get_user_list()
    if l is not None:
        l.delete()
        message = 'list \"{name}\" deleted'.format(name=name)
    else:
        message = 'can\'t delete a list that doesn\'t exist!'
    return message


def add_item(from_number, full_message):
    cmd, list_name, item = full_message.split(' ', maxsplit=2)

    l = get_user_list(from_number, list_name)
    if l is not None:
        l.items.append(item)
        l.save()
        message = list_contents(from_number, 'ls {list_name}'.format(list_name=list_name))
    else:
        message = 'couldn\'t add \"{item}\" to \"{list}\"'.format(item=item, list=list_name)
    return message


def remove_item(from_number, full_message):
    cmd, list_name, index = full_message.split(' ')
    # 1 indexed in text, 0 indexed in mongo
    index = int(index) - 1
    l = get_user_list(from_number, list_name)
    if l is not None and -1 < index < len(l.items):
        l.items.pop(index)
        l.save()
        message = list_contents(from_number, 'ls {list_name}'.format(list_name=list_name))
    else:
        message = 'couldn\'t remove item {index} from \"{list_name}\"'.format(index=index, list_name=list_name)
    return message


def list_contents(from_number, full_message):
    cmd, list_name = full_message.split(' ', maxsplit=2)
    l = get_user_list(from_number, list_name)
    if l is not None:
        length = len(l.items) if l.items else 0
        message = '\n'.join(["{0}. {1}".format(i + 1, l.items[i]) for i in range(length)]) if length > 0 else  \
            'Nothing. :('
    else:
        message = 'you don\'t have list called {list_name}'.format(list_name=list_name)
    return message


def add_sub(from_number, full_message):
    cmd, list_name, phone = full_message.split(' ')
    phone = phonenumbers.format_number(phonenumbers.parse(phone, 'US'), phonenumbers.PhoneNumberFormat.E164)
    l = get_user_list(from_number, list_name)
    if l is not None:
        l.subs.append(str(phone))
        l.save()
        message = 'added \"{phone}\" to \"{list_name}\"'.format(phone=phone, list_name=list_name)
    else:
        message = 'unable to add {phone} to {list_name}'.format(phone=phone,list_name=list_name)
    return message


def remove_sub(from_number, full_message):
    cmd, list_name, index = full_message.split(' ')
    index = int(index) - 1
    l = get_user_list(from_number, list_name)
    if l is not None and -1 < index < len(l.subs):
        phone = l.subs[index]
        l.subs.remove(phone)
        l.save()
        message = 'removed \"{ohone}\" from \"{list_name}\"'.format(phone=phone, list_name=list_name)
    else:
        message = 'unable to remove \"{phone}\" from \"{list_name}\"'.format(phone=phone, list_name=list_name)
    return message


def list_subs(from_number, full_message):
    cmd, list_name = full_message.split(' ')
    l = get_user_list(from_number, list_name)
    if l is not None:
        length = len(l.subs) if l.subs else 0
        message = '\n'.join(["{0}. {1}".format(i + 1, l.items[i]) for i in range(length)]) if length > 0 else  \
            'No subscribers'
    else:
        message = 'unable to list subscribers'
    return message


def stop(from_number, full_message):
    lists = Lists.objects(subs=from_number)
    for temp in lists:
        temp.subs.remove(from_number)
        temp.save()

    return 'thanks for using smsremind'


def help_message(from_number, full_message):
    return r"""
    SMSRemind
    commons ops:
    lists
    create [list]
    delete [list]
    add [list] [item]
    rm [list] [item index]
    ls [list]
    sub [list] [phone]
    lsub [list]
    unsub [list] [phone index]
    s
    h
    """

commands = {
    'lists': show_lists,
    'create': create_list,
    'delete': delete_list,
    'add': add_item,
    'rm': remove_item,
    'ls': list_contents,
    'sub': add_sub,
    'unsub': remove_sub,
    'lsub': list_subs,
    's': stop,
    'h': help_message,
}


def build_reply(message):
    resp = MessagingResponse()
    resp.message(message)
    return str(resp)


@app.route('/', methods=['GET', 'POST'])
def listener():
    message = request.values.get('Body', 'help').strip()
    cmd = message.split(' ')[0].lower()
    return build_reply(commands[cmd](request.values.get('From', None), message))

if __name__ == '__main__':
    debug = not app.config['CONFIGURATION'] == "PRODUCTION"
    app.run(debug=debug, port=app.config['PORT'], host="0.0.0.0")
