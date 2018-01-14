from flask import Blueprint, render_template, request, redirect, url_for
from mymetrics.vain_api import VainAPI, itemname_to_cssreadable, \
    particularplayer_from_singlematch

# mod = Blueprint('vain', __name__, url_prefix='/vain')
mod = Blueprint('vain', __name__, subdomain='vainlab')


@mod.route('/')
def index():
    return render_template('vain/index.html')


@mod.route('/_singleplayer/', methods=['POST', 'GET'])
@mod.route('/_singleplayer/<reg>/<ign>/', methods=['POST', 'GET'])
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


@mod.route('/_player/', methods=['POST', 'GET'])
@mod.route('/_player/<ign>/', methods=['POST', 'GET'])
def _player(ign=None):
    if request.method == 'GET':
        if ign:
            player_matches = VainAPI().player_matches_wo_region(ign)
            matches = player_matches['matches']
            player_id = ''
            for k, v in player_matches['players'].items():
                if v['name'] == ign:
                    player_id = k
                    break
        else:
            matches = {'errors': 'Lacks reg and ign'}
            player_id = ''
        return render_template('vain/singleplayer.html',
                               matches=matches, player_id=player_id,
                               players=player_matches['players'],
                               itemname_to_cssreadable=itemname_to_cssreadable,
                               this_player=particularplayer_from_singlematch)
    else:
        ign = request.form['ign']
        return redirect(url_for('vain.player') + f'{ign}/')


@mod.route('/player/', methods=['POST', 'GET'])
@mod.route('/player/<ign>/', methods=['POST', 'GET'])
def player(ign=None):
    if request.method == 'GET':
        if ign:
            player_matches = VainAPI().player_matches_wo_region(ign)
            matches = player_matches['matches']
            player_id = ''
            for k, v in player_matches['players'].items():
                if v['name'] == ign:
                    player_id = k
                    break
        else:
            matches = {'errors': 'Lacks reg and ign'}
            player_id = ''
        return render_template('vain/matches.html',
                               matches=matches, player_id=player_id,
                               players=player_matches['players'],
                               itemname_to_cssreadable=itemname_to_cssreadable,
                               this_player=particularplayer_from_singlematch)
    else:
        ign = request.form['ign']
        return redirect(url_for('vain.player') + f'{ign}/')


@mod.route('/_debug')
def static():
    return render_template('vain/galary-tiers.html')
