from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def listener():
    print("hello, world")

if __name__ == '__main__':
    app.run(debug=True)
