import os
from flask import Flask, render_template, request, session, json


def create_app(test_config=None):
    # create, configure
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'emu.sqlite'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import interpret

    @app.route('/app')
    def main_page():
        return render_template('emu.html', page_title="emu")

    @app.route('/entry', methods=['POST'])
    def process_input():
        input = request.form['text']
        result = interpret.interpret(input)
        return json.jsonify(result)

    return app
