from flask import (Flask, make_response, render_template, request,  # noqa
                   send_file)

from applications import vain
from mymetrics.environment import when_development

# デバッグをしたい場合
# import pdb;  pdb.set_trace()


app = Flask(__name__)
# Blueprints to use depending on environment (dev or prod)
if when_development():
    mods = [vain.mod, ]
    # app.config['SERVER_NAME'] = 'localhost:5000'
else:
    mods = [vain.mod, ]
    # app.config['SERVER_NAME'] = 'gitshell.net'
# Deploy blueprints
for m in mods:
    app.register_blueprint(m)


if __name__ == '__main__':
    app.run(debug=when_development())
