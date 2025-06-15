from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "6cabbd73a8c87af79fe9dee6e92d9305"
from my_web import route
