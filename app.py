import json

from flask import Flask, render_template, session, url_for, redirect

from access import group_required
from blueprint_query.route import blueprint_query
from auth.route import blueprint_auth
from blueprint_report.route import blueprint_report
from basket.route_cache import blueprint_order
from typing import List, Callable

app = Flask(__name__)
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_query, url_prefix='/queries')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_order, url_prefix='/order')

app.config['db_config'] = json.load(open('data_files/dbconfig.json'))
app.config['cache_config'] = json.load(open('data_files/cache.json'))
app.config['access_config'] = json.load(open('data_files/access.json'))
app.config['fields_name'] = json.load(open('data_files/fields.json', encoding='UTF-8'))
app.config['queries_list'] = json.load(open('data_files/queries.json', encoding='UTF-8'))

with open('data_files/reports.json', 'r', encoding='UTF-8') as f:
    reports = json.load(f)
    reports_list = []
    reports_url = {}

    for i in reports:
        reports_list.append({'rep_name': i['rep_name'], 'rep_id': i['rep_id']})
        reports_url[i['rep_id']] = {'create_rep': i['url']['create_rep'], 'view_rep': i['url']['view_rep']}

    app.config['reports_list'] = reports_list
    app.config['reports_url'] = reports_url


@app.route('/')
def menu_choice():
    if 'user_id' in session:
        if session.get('user_group', None):
            return render_template('lk_home.html', active_page='home', user=session.get('user_login'))
        else:
            return render_template('external_user_menu.html', user=session.get('user_login'))
    else:
        return redirect(url_for('blueprint_auth.start_auth'))


@app.route('/exit')
def exit_func():
    login = session.get('user_login')

    if 'user_id' in session:
        session.clear()

    return render_template('exit.html', user=login)


def add_blueprint_access_handler(f_app: Flask, blueprint_names: List[str], handler: Callable) -> Flask:
    for view_func_name, view_func in app.view_functions.items():
        view_func_parts = view_func_name.split('.')

        if len(view_func_parts) > 1:
            view_blueprint = view_func_parts[0]

            if view_blueprint in blueprint_names:
                view_func = handler(view_func)
                f_app.view_functions[view_func_name] = view_func
    return f_app


if __name__ == '__main__':
    app = add_blueprint_access_handler(app, ['bp_report'], group_required)
    app.run(host='127.0.0.1', port=5001)
