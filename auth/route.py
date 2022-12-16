import os
from typing import Optional, Dict
from flask import Blueprint, request, render_template, current_app, session, redirect, url_for

from db_context_manager import DBConnection
from db_work import select_dict
from sql_provider import SQLProvider

blueprint_auth = Blueprint('bp_auth', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET', 'POST'])
def start_auth():
    if request.method == 'GET':
        return render_template('login.html', message='')
    else:
        login = request.form.get('login')
        password = request.form.get('password')

        if login:
            user_info = define_user(login, password)

            if user_info:
                user_dict = user_info[0]
                session['user_id'] = user_dict['user_id']
                session['user_group'] = user_dict['user_group']
                session['user_login'] = user_dict['login']
                session.permanent = True

                return redirect(url_for('menu_choice'))
            else:
                toast_message = 'Пользователь не найден'
        else:
            toast_message = 'Повторите ввод'

    return render_template('login.html', show_toast=True, toast_type='danger',
                           toast_title='Ошибка', toast_message=toast_message)


def define_user(login: str, password: str) -> Optional[Dict]:
    sql_internal = provider.get('internal_user.sql', login=login, password=password)
    sql_external = provider.get('external_user.sql', login=login, password=password)

    user_info = None

    for sql_search in [sql_internal, sql_external]:
        user_info = select_dict(current_app.config['db_config'], sql_search)

        if user_info:
            break

    return user_info


@blueprint_auth.route('/reg', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        toast_type = ''
        toast_title = ''
        toast_message = ''

        login = request.form.get('login')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')

        if login and password and repeat_password and password == repeat_password:
            db_config = current_app.config['db_config']

            with DBConnection(db_config) as cursor:
                if cursor is None:
                    raise ValueError('Курсор не создан')

                _sql = provider.get('create_external.sql', login=login, password=password)
                result = cursor.execute(_sql)

                if result:
                    toast_type = 'success'
                    toast_title = 'Успешно'
                    toast_message = 'Пользователь создан'
                else:
                    toast_type = 'danger'
                    toast_title = 'Ошибка'
                    toast_message = 'Что-то пошло не так'

        else:
            toast_type = 'danger'
            toast_title = 'Ошибка'
            toast_message = 'Повторите ввод'

        return render_template('register.html', show_toast=True, toast_type=toast_type,
                               toast_title=toast_title, toast_message=toast_message)
