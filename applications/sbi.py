from flask import Blueprint, render_template, request, send_file
from mymetrics.sbi_trade_history import SbiAnalyzer
from mymetrics.analytics import track_event
import pandas as pd
from io import BytesIO
# デバッグをしたい場合
# import pdb;  pdb.set_trace()


mod = Blueprint('sbi', __name__, url_prefix='/sbi')


@mod.route('/')
def sbi():
    """ analyze sbi history """
    track_event('sbi', 'get')

    buttons = [
        ('exec', '分析実行', 'RR分析＆グラフ描画'),
        ('rearrange', 'データ整形', '整形されたデータをダウンロード'),
    ]
    return render_template('sbi.html', buttons=buttons)


@mod.route('/sbi_button', methods=['POST'])
def sbi_button():
    """ calculate sbi risk riward """

    ifile = request.files['file']
    sbi = SbiAnalyzer(ifile)

    if request.form['action'] == 'exec':
        track_event('sbi', 'plt')
        bk_script, bk_div, bk_v = sbi.bokeh_plot_history()
        rr = pd.DataFrame(sbi.evaluate_risk_reward(ja=True)).T
        rr_table = rr.to_html(classes="table", header=False, index=False)
        return render_template('sbi-history.html',
                               rr_table=rr_table,
                               bk_script=bk_script, bk_div=bk_div, bk_v=bk_v)
    elif request.form['action'] == 'rearrange':
        track_event('sbi', 'rearrange')
        ofile = sbi.df.to_csv().encode('utf-8')
        return send_file(BytesIO(ofile), attachment_filename='SBIhistory.csv',
                         as_attachment=True)
