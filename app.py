from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/about')
def about():
    accounts = [
        ('Qiita', 'https://qiita.com/qiugits'),
        ('Github', 'https://github.com/qiugits'),
    ]
    return render_template('about.html', accounts=accounts)


if __name__ == '__main__':
    app.run(debug=True)
