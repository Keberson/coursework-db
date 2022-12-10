import os.path

from access import login_required, group_required
from flask import Blueprint, request, render_template, current_app, url_for
from db_work import select
from sql_provider import SQLProvider

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/queries', methods=['GET', 'POST'])
def queries():
    input_type = request.args.to_dict()['base']

    if request.method == 'GET':
        return render_template('lk_queries.html', table=input_type, message='')
    else:
        input_name = request.form.get('input_name')

        if input_name and input_type:
            _sql = provider.get('template.sql', input_table=input_type, input_name=input_name)
            client_result, schema = select(current_app.config['db_config'], _sql)

            return render_template('lk_result.html', schema=[current_app.config['fields_name'][i] for i in schema],
                                   result=client_result,
                                   url=url_for('bp_query.queries', base=input_type),
                                   title=f'Результат поиска \"{input_name}\"')
        else:
            return render_template('lk_queries.html', table=input_type, message='Повторите ввод')


@blueprint_query.route('/select', methods=['GET', 'POST'])
def select_query():
    if request.method == 'GET':
        return render_template('lk_select.html', select_list=current_app.config['queries_list'],
                               message='')
    else:
        input_select = request.form.get('input_select')

        if input_select:
            _sql = provider.get(f'easy_request_{input_select}.sql')
            client_result, schema = select(current_app.config['db_config'], _sql)

            return render_template('lk_result.html', schema=[current_app.config['fields_name'][i] for i in schema],
                                   result=client_result,
                                   url=url_for('bp_query.select_query'),
                                   title=current_app.config["queries_list"][input_select])
        else:
            return render_template('lk_select.html', select_list=current_app.config['queries_list'],
                                   message='Повторите ввод')
