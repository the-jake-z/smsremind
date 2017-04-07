from flask import Flask, request, redirect
from mongoengine import *
from config import *

app = Flask(__name__)
app.config.from_object(os.environ.get('CONFIG_CLASS', 'config.DevelopmentConfig'))

connect(host=app.config['MONGODB_SETTINGS']['host'] or None)


def Lists(Document):
    subs = ListField(StringField())
    items = ListField(StringField())


@app.route('/', methods=['GET','POST'])
def listener():
    print("hello, world")
    return "success"

if __name__ == '__main__':
    app.run(debug=True)
