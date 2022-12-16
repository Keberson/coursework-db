import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_context_manager import DBConnection
from db_work import select_dict, call_proc
from sql_provider import SQLProvider
from cache.wrapper import fetch_from_cache, fetch_from_cache_force

blueprint_order = Blueprint('bp_order', __name__, template_folder='templates', static_folder='static')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_order.route('/', methods=['GET', 'POST'])
def order_index():
    db_config = current_app.config['db_config']
    cache_config = current_app.config['cache_config']
    cached_select = fetch_from_cache('all_items_cached', cache_config)(select_dict)

    if request.method == 'GET':
        sql = provider.get('all_items.sql')
        items = cached_select(db_config, sql)
        basket_items = session.get('basket', {})
        return render_template('basket_order_list.html', items=items, basket=basket_items)
    else:
        id_detail = request.form['id_detail']
        sql = provider.get('all_items.sql')
        items = select_dict(db_config, sql)

        add_to_basket(id_detail, items)

        return redirect(url_for('bp_order.order_index'))


def add_to_basket(id_detail: str, items: dict):
    item_description = [item for item in items if str(item['id_detail']) == str(id_detail)]
    item_description = item_description[0]
    curr_basket = session.get('basket', {})

    if id_detail in curr_basket:
        curr_basket[id_detail]['amount'] = curr_basket[id_detail]['amount'] + 1
    else:
        curr_basket[id_detail] = {
            'id_detail': id_detail,
            'name': item_description['name'],
            'material': item_description['material'],
            'weight': item_description['weight'],
            'price': item_description['price'],
            'quantity_available': item_description['quantity_available'],
            'amount': 1
        }

        session['basket'] = curr_basket
        session.permanent = True
    return True


@blueprint_order.route('/delete', methods=['GET', 'POST'])
def delete_from_basket():
    curr_basket = session.get('basket', {})
    curr_basket.pop(request.args['id_detail'])
    session['basket'] = curr_basket
    session.permanent = True

    return redirect(url_for('bp_order.order_index'))


@blueprint_order.route('/amount', methods=['GET', 'POST'])
def edit_amount_basket():
    curr_basket = session.get('basket', {})

    if 'value' in request.args:
        id_detail = request.args['id_detail']
        amount = curr_basket[id_detail]['amount'] + int(request.args['value'])
    else:
        id_detail = request.form['detail']
        amount = int(request.form['amount'])

    max_amount = int(curr_basket[id_detail]['quantity_available'])

    amount = 1 if amount < 1 else amount
    amount = max_amount if amount > max_amount else amount

    curr_basket[id_detail]['amount'] = amount

    session['basket'] = curr_basket
    session.permanent = True

    return redirect(url_for('bp_order.order_index'))


@blueprint_order.route('/clear-basket')
def clear_basket():
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('bp_order.order_index'))


@blueprint_order.route('/save_order', methods=['GET', 'POST'])
def save_order():
    user_id = session.get('user_id')
    current_basket = session.get('basket', {})

    if len(current_basket) == 0:
        return render_template('error.html')

    order_id = save_order_with_list(current_app.config['db_config'], user_id, current_basket)

    if order_id:
        items = [item for item in current_basket.values()]
        total = sum([item['amount'] * item['price'] for item in items])
        session.pop('basket')

        sql = provider.get('all_items.sql')
        res = fetch_from_cache_force('all_items_cached', current_app.config['cache_config'])(select_dict)(
            current_app.config['db_config'], sql)

        return render_template('order_created.html', order_id=order_id, items=items, total=total)
    else:
        return render_template('error.html')


def save_order_with_list(dbconfig: dict, user_id: int, current_basket: dict):
    with DBConnection(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')

        items = [item for item in current_basket.values()]
        total = sum([item['amount'] * item['price'] for item in items])
        _sql1 = provider.get('insert_order.sql', user_id=user_id, costs=total)
        result1 = cursor.execute(_sql1)

        if result1 == 1:
            _sql2 = provider.get('select_order_id.sql', user_id=user_id)
            cursor.execute(_sql2)
            order_id = cursor.fetchall()[0][0]

            if order_id:
                for key in current_basket:
                    amount = current_basket[key]['amount']
                    _sql3 = provider.get('insert_order_list.sql', order_id=order_id, detail_id=key,
                                         amount=amount)
                    cursor.execute(_sql3)

                res = call_proc(current_app.config['db_config'], 'refresh', order_id)

                return order_id
