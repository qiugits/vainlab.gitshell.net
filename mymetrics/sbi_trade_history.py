# coding: utf-8
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh import __version__ as _bokeh_version


class SbiAnalyzer:
    """ SBI History Analyzer """
    def __init__(self, _fname):
        self.df = self._rearrange_trade_data(_fname)

    def _rearrange_trade_data(self, _fname):
        """
        parameter: fileIO (or filename. That doesn't matter to np)
        returns:   df
        """

        _dtype = {
            '約定価格': 'int32',
            '約定数量': 'int16',
            '手数料': 'int16',
            '消費税': 'int16',
            '約定金額': 'int32',
            '受渡金額': 'int32',
        }
        df = pd.read_csv(_fname, encoding='Shift-JIS', skiprows=5,
                         dtype=_dtype)

        # df[[1, 4,5,6, 14, 17]]
        _df = df[['約定日時', '取引', '約定価格', '約定数量', '新規建単価', '決済損益']]

        def gen_row(): return ['', '', 0, 0, '', 0, 0, 0]
        _columns = ['order time', 'settle time', 'order price', 'settle price',
                    'position', 'tickets', 'result', 'profit/loss']
        en = {'新規買': 'K', '新規売': 'U'}
        tmp = []
        for i in reversed(_df.values):
            if '決済' in i[1]:
                t = gen_row()
                t[1], t[2], t[3], t[5], t[7] =\
                    i[0], int(i[4]), i[2], i[3], int(i[5])
                if '売' in i[1]:
                    t[4] = 'K'
                    t[6] = t[3] - t[2]
                elif '買' in i[1]:
                    t[4] = 'U'
                    t[6] = t[2] - t[3]
                tmp.append(t)
        for i in reversed(_df.values):
            if '新規' in i[1]:
                for t in reversed(tmp):
                    if not t[0] and t[2] == i[2] and en[i[1]] == t[4]:
                        t[0] = i[0]
                        break
                else:
                    print(i)
        # print(*tmp[:5], sep='\n')
        return pd.DataFrame(tmp, columns=_columns)

    def evaluate_risk_reward(self, ja=False):
        cr = self.df[['result']].values
        _win = list(filter(lambda x: x > 0, cr))
        _lose = list(filter(lambda x: x < 0, cr))
        ave_win = np.average(_win)
        ave_lose = np.average(_lose)
        num_win = len(_win)
        num_lose = len(_lose)
        win_rate = num_win / (num_win + num_lose)
        risk_reward = ave_win / abs(ave_lose)
        if ja:
            rr = [
                ('平均利益', round(ave_win, 2)),
                ('平均損失', round(ave_lose, 2)),
                ('勝ち数', num_win),
                ('負け数', num_lose),
                ('勝率', f'{ round(win_rate * 100, 2)}%'),
                ('リスク・リワード', round(risk_reward, 4))
            ]
        else:
            rr = [
                ('ave_win', ave_win),
                ('ave_lose', ave_lose),
                ('num_win', num_win),
                ('num_lose', num_lose),
                ('win_rate', win_rate),
                ('risk_reward', risk_reward)
            ]
        return rr

    # def plot_profit_history(self):
    #     res = self.df
    #     cs_res = np.cumsum(res[['result']].values.T)
    #     cs_pro = np.cumsum(res[['profit/loss']].values.T) / 100
    #     # print(max(cs_res) - min(cs_res))
    #     plt.plot(cs_res)
    #     plt.plot(cs_pro)
    #     return plt

    def bokeh_plot_history(self):
        res = self.df
        cs_res = np.cumsum(res[['result']].values.T)
        cs_pro = np.cumsum(res[['profit/loss']].values.T) / 100
        # print(max(cs_res) - min(cs_res))
        x = np.arange(len(cs_pro))
        p = figure()
        p.line(x, cs_res, line_width=1.5,
               line_dash='dotted', line_color='orange')
        p.line(x, cs_pro, line_width=2)
        script, div = components(p)
        return script, div, _bokeh_version
