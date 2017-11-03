from flask import Flask, render_template, request, send_file
from mymetrics.sbi_trade_history import rearrange_trade_data, evaluate_risk_reward
from mymetrics.analytics import track_event
import pandas as pd
from io import BytesIO

app = Flask(__name__)


@app.route('/')
@app.route('/about')
def about():
    """ about """
    track_event('about', 'get')

    accounts = [
        ('Qiita', 'https://qiita.com/qiugits'),
        ('Github', 'https://github.com/qiugits'),
    ]
    return render_template('about.html', accounts=accounts)


@app.route('/sbi', methods=['GET', 'POST'])
def sbi():
    """ analyze sbi history """
    track_event('sbi', 'post/get')

    if request.method == 'GET':
        return render_template('sbi.html')
    else:  # == 'POST'
        ifile = request.files['file']
        df = pd.read_csv(ifile, encoding='Shift-JIS', skiprows=5)
        res = rearrange_trade_data(df)
        ofile = res.to_csv().encode('utf-8')
        return send_file(BytesIO(ofile), attachment_filename='outfile.csv',
                         as_attachment=True)


@app.route('/sbi_calc_rr', methods=['POST'])
def sbi_calc_rr():
    """ calculate sbi risk riward """
    track_event('sbi', 'post-rr')

    if request.method == 'POST':
        ifile = request.files['file']
        df = pd.read_csv(ifile, encoding='Shift-JIS', skiprows=5)
        res = rearrange_trade_data(df)
        rr = evaluate_risk_reward(res)
        return render_template('sbi.html', risk_reward=rr)



if __name__ == '__main__':
    app.run(debug=True)
