import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_context_manager import DBConnection
from db_work import select_dict
from sql_provider import SQLProvider

blueprint_edit = Blueprint('bp_edit', __name__, template_folder="templates")
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_edit.route('/details', methods=['GET', 'POST'])
def all_products():
    if request.method == 'GET':
        db_config = current_app.config['db_config']
        _sql = provider.get('all_details.sql')
        items = select_dict(db_config, _sql)

        return render_template('all_details.html', items=items)
    else:
        db_config = current_app.config['db_config']
        action = request.form.get('action')
        id_detail = request.form.get('detail_id')

        if action == 'edit':
            return redirect(url_for('bp_edit.edit_detail', detail_id=id_detail))
        if action == 'delete':
            with DBConnection(db_config) as cursor:
                if cursor is None:
                    raise ValueError('Курсор не создан')
                _sql = provider.get('delete_detail.sql', id_detail=id_detail)
                result1 = cursor.execute(_sql)

                if result1:
                    toast_title = 'Успешно'
                    toast_message = 'Товар удалён'
                    toast_type = 'success'
                else:
                    toast_title = 'Ошибка'
                    toast_message = 'Что-то пошло не так'
                    toast_type = 'primary'

            db_config = current_app.config['db_config']
            _sql = provider.get('all_details.sql')
            items = select_dict(db_config, _sql)

            return render_template('all_details.html', items=items, show_toast=True, toast_title=toast_title,
                                   toast_message=toast_message, toast_type=toast_type)


@blueprint_edit.route('/edit_details', methods=['GET', 'POST'])
def edit_detail():
    if request.method == 'GET':
        id_detail = request.args['detail_id']
        _sql = provider.get('get_detail_by_id.sql', id_detail=id_detail)
        detail = select_dict(current_app.config['db_config'], _sql)[0]

        return render_template('detail_update.html', detail=detail)
    else:
        db_config = current_app.config['db_config']
        id_detail = request.form.get('id_detail')
        input_name = request.form.get('input_name')
        input_material = request.form.get('input_material')
        input_weight = request.form.get('input_weight')
        input_price = request.form.get('input_price')
        input_quantity = request.form.get('input_quantity')

        if id_detail and input_name and input_material and input_material and input_weight and input_price and \
                input_quantity:
            with DBConnection(db_config) as cursor:
                if cursor is None:
                    raise ValueError('Курсор не создан')

                _sql = provider.get('update_detail.sql', id_detail=id_detail, detail_name=input_name,
                                    detail_material=input_material, detail_weight=input_weight,
                                    detail_price=input_price,
                                    detail_quantity=input_quantity)
                result = cursor.execute(_sql)

                if result:
                    toast_title = 'Успешно'
                    toast_message = 'Товар обновлен'
                    toast_type = 'success'
                else:
                    toast_title = 'Ошибка'
                    toast_message = 'Что-то пошло не так'
                    toast_type = 'primary'
        else:
            toast_title = 'Ошибка'
            toast_message = 'Повторите ввод'
            toast_type = 'danger'

        _sql = provider.get('get_detail_by_id.sql', id_detail=id_detail)
        detail = select_dict(current_app.config['db_config'], _sql)[0]

        return render_template('detail_update.html', detail=detail, show_toast=True, toast_title=toast_title,
                               toast_message=toast_message, toast_type=toast_type)


@blueprint_edit.route('/insert_details', methods=['GET', 'POST'])
def insert_detail():
    toast_title = ''
    toast_message = ''
    toast_type = ''

    if request.method == 'GET':
        return render_template('detail_insert.html')
    else:
        db_config = current_app.config['db_config']
        input_name = request.form.get('input_name')
        input_material = request.form.get('input_material')
        input_weight = request.form.get('input_weight')
        input_price = request.form.get('input_price')
        input_quantity = request.form.get('input_quantity')

        if input_name and input_material and input_weight and input_price and input_quantity:
            with DBConnection(db_config) as cursor:
                if cursor is None:
                    raise ValueError('Курсор не создан')

                _sql = provider.get('insert_detail.sql', detail_name=input_name,
                                    detail_material=input_material, detail_weight=input_weight,
                                    detail_price=input_price,
                                    detail_quantity=input_quantity)
                result = cursor.execute(_sql)

                if result:
                    toast_title = 'Успешно'
                    toast_message = 'Товар добавлен'
                    toast_type = 'success'
                else:
                    toast_title = 'Ошибка'
                    toast_message = 'Что-то пошло не так'
                    toast_type = 'primary'
        else:
            toast_title = 'Ошибка'
            toast_message = 'Повторите ввод'
            toast_type = 'danger'

        return render_template('detail_insert.html', show_toast=True, toast_title=toast_title,
                               toast_message=toast_message, toast_type=toast_type)


@blueprint_edit.route('/internals', methods=['GET', 'POST'])
def all_internals():
    if request.method == 'GET':
        db_config = current_app.config['db_config']
        _sql = provider.get('all_internals.sql')
        items = select_dict(db_config, _sql)

        return render_template('all_internals.html', items=items)
    else:
        db_config = current_app.config['db_config']
        action = request.form.get('action')
        user_id = request.form.get('user_id')

        if action == 'edit':
            return redirect(url_for('bp_edit.edit_internal', user_id=user_id))
        if action == 'delete':
            with DBConnection(db_config) as cursor:
                if cursor is None:
                    raise ValueError('Курсор не создан')
                _sql = provider.get('delete_internal.sql', user_id=user_id)
                result1 = cursor.execute(_sql)

                if result1:
                    toast_title = 'Успешно'
                    toast_message = 'Пользователь удален'
                    toast_type = 'success'
                else:
                    toast_title = 'Ошибка'
                    toast_message = 'Что-то пошло не так'
                    toast_type = 'primary'

            db_config = current_app.config['db_config']
            _sql = provider.get('all_internal.sql')
            items = select_dict(db_config, _sql)

            return render_template('all_internals.html', items=items, show_toast=True, toast_title=toast_title,
                                   toast_message=toast_message, toast_type=toast_type)


@blueprint_edit.route('/edit_internal', methods=['GET', 'POST'])
def edit_internal():
    if request.method == 'GET':
        user_id = request.args['user_id']
        _sql = provider.get('get_internal_by_id.sql', user_id=user_id)
        user = select_dict(current_app.config['db_config'], _sql)[0]

        return render_template('internal_update.html', user=user)
    else:
        db_config = current_app.config['db_config']
        user_id = request.form.get('user_id')
        input_login = request.form.get('input_login')
        input_group = request.form.get('input_group')
        input_password = request.form.get('input_password')

        if user_id and input_login and input_group and input_password:
            with DBConnection(db_config) as cursor:
                if cursor is None:
                    raise ValueError('Курсор не создан')

                _sql = provider.get('update_internal.sql', user_id=user_id, input_login=input_login,
                                    input_group=input_group, input_password=input_password)
                result = cursor.execute(_sql)

                if result:
                    toast_title = 'Успешно'
                    toast_message = 'Пользователь обновлен'
                    toast_type = 'success'
                else:
                    toast_title = 'Ошибка'
                    toast_message = 'Что-то пошло не так'
                    toast_type = 'primary'
        else:
            toast_title = 'Ошибка'
            toast_message = 'Повторите ввод'
            toast_type = 'danger'

        _sql = provider.get('get_internal_by_id.sql', user_id=user_id)
        _sql = provider.get('get_internal_by_id.sql', user_id=user_id)
        user = select_dict(current_app.config['db_config'], _sql)[0]

        return render_template('internal_update.html', user=user, show_toast=True, toast_title=toast_title,
                               toast_message=toast_message, toast_type=toast_type)


@blueprint_edit.route('/insert_internal', methods=['GET', 'POST'])
def insert_internal():
    toast_title = ''
    toast_message = ''
    toast_type = ''

    if request.method == 'GET':
        return render_template('internal_insert.html')
    else:
        db_config = current_app.config['db_config']
        input_login = request.form.get('input_login')
        input_group = request.form.get('input_group')
        input_password = request.form.get('input_password')

        if input_login and input_group and input_password:
            with DBConnection(db_config) as cursor:
                if cursor is None:
                    raise ValueError('Курсор не создан')

                _sql = provider.get('insert_internal.sql', input_login=input_login,
                                    input_group=input_group, input_password=input_password)
                result = cursor.execute(_sql)

                if result:
                    toast_title = 'Успешно'
                    toast_message = 'Пользователь добавлен'
                    toast_type = 'success'
                else:
                    toast_title = 'Ошибка'
                    toast_message = 'Что-то пошло не так'
                    toast_type = 'primary'
        else:
            toast_title = 'Ошибка'
            toast_message = 'Повторите ввод'
            toast_type = 'danger'

        return render_template('internal_insert.html', show_toast=True, toast_title=toast_title,
                               toast_message=toast_message, toast_type=toast_type)

