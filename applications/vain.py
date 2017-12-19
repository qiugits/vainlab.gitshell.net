from flask import Blueprint, render_template

mod = Blueprint('vain', __name__, url_prefix='/vain')


@mod.route('/')
def index():
    return render_template('vain/index.html')
