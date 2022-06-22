from flask import Flask, jsonify, abort
from json import load
import pathlib

app = Flask(__name__)
with open(pathlib.Path(__file__).parent.resolve() / 'static/blueprints.json', 'r') as f:
    blueprints = load(f)


@app.route('/')
def show_index():
    return jsonify({
        'available_routes': [
            {
                'path': '/blueprints',
                'description': 'Return all blueprints'
            },
            {
                "path": "/blueprints/<category>",
                "description": "Return all blueprints in the requested category"
            }
        ]
    })

@app.route('/blueprints/<string:category>')
@app.route('/blueprints/<string:category>/')
@app.route('/blueprints', defaults={'category': None})
@app.route('/blueprints/', defaults={'category': None})
def show_blueprints(category):
    if not category:
        return jsonify(blueprints)
    else:
        try:
            return jsonify(blueprints[category])
        except KeyError:
            return jsonify({'error': {'error_code': 404, 'error_message': f"Category not found: {category}"}}), 404


if __name__ == '__main__':
    app.run('0.0.0.0', debug=False)
