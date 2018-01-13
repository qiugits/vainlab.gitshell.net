from flask import Flask, render_template, request, send_file, make_response  # noqa
from datetime import datetime
from applications import sbi, vain  # noqa
from mymetrics.environment import if_is_development
# デバッグをしたい場合
# import pdb;  pdb.set_trace()


app = Flask(__name__)
# Blueprints to use depending on environment (dev or prod)
# Development stage
if if_is_development():
    mods = [sbi.mod, vain.mod, ]
    app.config['SERVER_NAME'] = 'localhost:5000'
# Production stage
else:
    mods = [sbi.mod, vain.mod, ]
    app.config['SERVER_NAME'] = 'gitshell.net'
# Deploy blueprints
for m in mods:
    app.register_blueprint(m)


@app.route('/')
@app.route('/about')
def about():
    """ about """
    accounts = [
        ('Qiita', 'https://qiita.com/qiugits'),
        ('Github', 'https://github.com/qiugits'),
    ]
    return render_template('about.html', accounts=accounts)


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml"""
    pages = []
    now = datetime.now()
    # static pages
    for rule in app.url_map.iter_rules():
        if 'GET' in rule.methods and len(rule.arguments) == 0:
            pages.append([rule.rule, now])

    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response


if __name__ == '__main__':
    app.run(debug=if_is_development())
