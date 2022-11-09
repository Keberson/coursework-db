import json

from flask import Flask, render_template, session, url_for, redirect
from blueprint_query.route import blueprint_query
from auth.route import blueprint_auth


app = Flask(__name__)
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_query, url_prefix='/queries')


app.config['db_config'] = json.load(open('data_files/dbconfig.json'))
app.config['access_config'] = json.load(open('data_files/access.json'))


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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)