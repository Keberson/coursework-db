import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_context_manager import DBConnection
from db_work import select_dict
from sql_provider import SQLProvider

blueprint_edit = Blueprint('bp_edit', __name__, template_folder="templates")
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_edit.route('/', methods=['GET', 'POST'])
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
            return redirect(url_for('bp_edit.edit_product', detail_id=id_detail))
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


@blueprint_edit.route('/edit', methods=['GET', 'POST'])
def edit_product():
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


@blueprint_edit.route('/insert_prod', methods=['GET', 'POST'])
def insert_prod():
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
