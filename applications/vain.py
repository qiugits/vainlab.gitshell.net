from flask import Blueprint, render_template, request, redirect, url_for
from mymetrics.vain_api import VainAPI, itemname_to_cssreadable, \
    particularplayer_from_singlematch

# mod = Blueprint('vain', __name__, url_prefix='/vain')
mod = Blueprint('vain', __name__, subdomain='vainlab')


@mod.route('/')
def index():
    return render_template('vain/index.html')


@mod.route('/singleplayer/', methods=['POST', 'GET'])
@mod.route('/singleplayer/<reg>/<ign>/', methods=['POST', 'GET'])
def single_player(reg=None, ign=None):
    if request.method == 'GET':
        if reg and ign:
            res = VainAPI().single_player(reg, ign)
            try:
                tier_str = ['銅', '銀', '金']
                jres = {
                    '取得時間': res['time'],
                    '地域': res['shrd'],
                    'IGN': res['name'],
                    # '連勝': res['wstr'],
                    # '連敗': res['lstr'],
                    '総合勝利数': res['wins'],
                    '階層': f'{(res["tier"]//3)+1}{tier_str[res["tier"]%3]}',
                    # 'ウィンター2017': res['elo8'],
                    'ELO': int(res['rnkp']),
                }
            except:
                jres = res
        else:
            jres = {'rslt': 'Lacks reg and ign'}
        return render_template('vain/singleplayer.html', res=jres)
    else:
        reg = request.form['reg']
        ign = request.form['ign']
        return redirect(url_for('vain.single_player') + f'{reg}/{ign}/')


@mod.route('/matches/', methods=['POST', 'GET'])
@mod.route('/matches/<reg>/<ign>/', methods=['POST', 'GET'])
def matches(reg=None, ign=None):
    if request.method == 'GET':
        if reg and ign:
            matches = VainAPI().matches(reg, ign)
            player_id = VainAPI().single_player(reg, ign).get('id', '')
        else:
            matches = {'rslt': 'Lacks reg and ign'}
            player_id = ''
        return render_template('vain/matches.html',
                               matches=matches, player_id=player_id,
                               itemname_to_cssreadable=itemname_to_cssreadable,
                               this_player=particularplayer_from_singlematch)
    else:
        reg = request.form['reg']
        ign = request.form['ign']
        return redirect(url_for('vain.matches') + f'{reg}/{ign}/')


@mod.route('/static_matches/')
def static():
    return render_template('vain/static_matches.html')
