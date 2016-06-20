
from flask import Flask
from flask_classy import FlaskView

app = Flask(__name__)

class HelloWorldView(FlaskView):
    def index(self):
        return "hello world"


HelloWorldView.register(app)

if __name__ == '__main__':
    app.run(debug=True)