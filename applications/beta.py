from flask import Blueprint, render_template
from flask_mail import Mail, Message

mod = Blueprint('beta', __name__, url_prefix='/beta')
mail = Mail(mod)

# mod.config.update(
#     MAIL_SERVER='gitshell.net',
#     MAIL_PORT=2500,
#     # MAIL_USE_TLS=True,
#     MAIL_USERNAME='qiu',
#     MAIL_PASSWORD='nn',
# )


@mod.route('/')
def index():
    pass


# @mod.route('/sendmail/')
# def sendmail():
#     msg = Message('Hello',
#                   sender='from@gitshell.net',
#                   recipients=['qiu.gits@gmail.com'])
#     mail.send(msg)
#
#     return 'sent!'
