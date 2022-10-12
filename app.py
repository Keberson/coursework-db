from flask import Flask, render_template, json
from blueprint_query.route import blueprint_query


app = Flask(__name__)
app.register_blueprint(blueprint_query, url_prefix='/queries')


with open('data_files/dbconfig.json', 'r') as f:
    db_config = json.load(f)
app.config['dbconfig'] = db_config


@app.route('/')
def index():
    return render_template('start_request.html')


@app.route('/goodbye')
def goodbye():
    return 'Bye'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)