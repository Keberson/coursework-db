import os.path

from flask import Blueprint, request, render_template, current_app
from db_work import select
from sql_provider import SQLProvider


blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/queries', methods=['GET', 'POST'])
def queries():
    if request.method == 'GET':
        return render_template('product_form.html')
    else:
        input_name = request.form.get('input_name')
        input_type = request.form.get('input_type')
        if input_name and input_type:
            _sql = provider.get('template.sql', input_table=input_type, input_name=input_name)
            print(_sql)
            client_result, schema = select(current_app.config['dbconfig'], _sql)

            return render_template('db_result.html', schema=schema, result=client_result)
        else:
            return "Repeat input"
