from flask import *
from db_work import select, call_proc
from access import login_required, group_required
from sql_provider import SQLProvider
import os

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/', methods=['GET', 'POST'])
def start_report():
    report_url = current_app.config['reports_url']

    if request.method == 'GET':
        return render_template('menu_report.html', report_list=current_app.config['reports_list'])
    else:
        rep_id = request.form.get('rep_id')

        if request.form.get('create_rep'):
            url_rep = report_url[rep_id]['create_rep']
        else:
            url_rep = report_url[rep_id]['view_rep']

        return redirect(url_for(url_rep))


@blueprint_report.route('/create_rep1', methods=['GET', 'POST'])
@group_required
def create_rep1():
    if request.method == 'GET':
        return render_template('report1.html', mode="create")
    else:
        id_det = request.form.get('input_id')
        rep_start = request.form.get('input_start')
        rep_end = request.form.get('input_end')

        if id_det and rep_start and rep_end:
            _sql = provider.get('rep1.sql', id_det=id_det, date_from=rep_start, date_to=rep_end)
            product_result, schema = select(current_app.config['db_config'], _sql)

            if not product_result:
                res = call_proc(current_app.config['db_config'], 'details_report', id_det, rep_start, rep_end)

                return render_template('report_created.html', to_url=url_for('bp_report.view_rep1', id_det=id_det,
                                                                             rep_start=rep_start, rep_end=rep_end))
            else:
                return redirect(url_for('bp_report.view_rep1', id_det=id_det, rep_start=rep_start, rep_end=rep_end))
        else:
            return render_template('report1.html', mode="create", message="Некорректный ввод!")


@blueprint_report.route('/view_rep1', methods=['GET', 'POST'])
@group_required
def view_rep1():
    if request.method == 'GET' and not request.args:
        return render_template('report1.html', mode="view")
    else:
        args = request.args

        id_det = args['id_det'] if 'id_det' in args and args['id_det'] else request.form.get('input_id')
        rep_start = args['rep_start'] if 'rep_start' in args and args['rep_start'] else request.form.get('input_start')
        rep_end = args['rep_end'] if 'rep_end' in args and args['rep_end'] else request.form.get('input_end')

        if id_det and rep_start and rep_end:
            _sql = provider.get('rep1.sql', id_det=id_det, date_from=rep_start, date_to=rep_end)
            product_result, schema = select(current_app.config['db_config'], _sql)

            return render_template('result_rep.html', schema=[current_app.config['fields_name'][i] for i in schema],
                                   result=product_result)
        else:
            return render_template('report1.html', mode="view", message="Некорректный ввод!")

@blueprint_report.route('/create_rep2', methods=['GET', 'POST'])
@group_required
def create_rep2():
    if request.method == 'GET':
        return render_template('report2.html', mode="create")
    else:
        rep_start = request.form.get('input_start')
        rep_end = request.form.get('input_end')

        if rep_start and rep_end:
            _sql = provider.get('rep2.sql', date_from=rep_start, date_to=rep_end)
            product_result, schema = select(current_app.config['db_config'], _sql)

            if not product_result:
                res = call_proc(current_app.config['db_config'], 'client_report', rep_start, rep_end)

                return render_template('report_created.html', to_url=url_for('bp_report.view_rep2',
                                                                             rep_start=rep_start, rep_end=rep_end))
            else:
                return redirect(url_for('bp_report.view_rep2', rep_start=rep_start, rep_end=rep_end))
        else:
            return render_template('report2.html', mode="create", message="Некорректный ввод!")



@blueprint_report.route('/view_rep2', methods=['GET', 'POST'])
@group_required
def view_rep2():
    if request.method == 'GET' and not request.args:
        return render_template('report2.html', mode="view")
    else:
        args = request.args

        rep_start = args['rep_start'] if 'rep_start' in args and args['rep_start'] else request.form.get('input_start')
        rep_end = args['rep_end'] if 'rep_end' in args and args['rep_end'] else request.form.get('input_end')

        if rep_start and rep_end:
            _sql = provider.get('rep2.sql', date_from=rep_start, date_to=rep_end)
            product_result, schema = select(current_app.config['db_config'], _sql)

            return render_template('result_rep.html', schema=[current_app.config['fields_name'][i] for i in schema],
                                   result=product_result)
        else:
            return render_template('report2.html', mode="view", message="Некорректный ввод!")

