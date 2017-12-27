from flask import Blueprint, render_template
from flask_mail import Mail, Message

mod = Blueprint('beta', __name__, url_prefix='/beta')
mail = Mail(mod)


@mod.route('/')
def index():
    pass


@mod.route('/sendmail/')
def sendmail():
    msg = Message('Hello',
                  sender='from@gitshell.net',
                  recipients=['qiu.gits@gmail.com'])
    mail.send(msg)

    return 'sent!'
