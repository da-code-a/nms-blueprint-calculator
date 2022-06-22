from flask import Flask, jsonify, render_template
from json import load
import pathlib

app = Flask(__name__)
with open(pathlib.Path(__file__).parent.resolve() / "static/blueprints.json", "r") as f:
    blueprints = load(f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/swagger")
def swagger_ui():
    return render_template("swagger.html")


@app.route("/swagger.json")
def swagger_json():
    return render_template("swagger.json")


@app.route("/api/blueprints/<string:category>")
@app.route("/api/blueprints", defaults={"category": None})
def show_blueprints(category):
    if not category:
        return jsonify(blueprints)
    else:
        try:
            return jsonify(blueprints[category])
        except KeyError:
            return (
                jsonify(
                    {
                        "error": {
                            "error_code": 404,
                            "error_message": f"Category not found: {category}",
                        }
                    }
                ),
                404,
            )


@app.route("/api/blueprints/<string:category>/<string:item>")
def show_item_blueprint(category, item):
    if category not in blueprints:
        return (
            jsonify(
                {
                    "error": {
                        "error_code": 404,
                        "error_message": f"Category not found: {category}",
                    }
                }
            ),
            404,
        )
    elif item not in blueprints[category]:
        return (
            jsonify(
                {
                    "error": {
                        "error_code": 404,
                        "error_message": f"Item not found: {category}/{item}",
                    }
                }
            ),
            404,
        )
    else:
        return jsonify(blueprints[category][item])


@app.route("/api/blueprints/categories")
def show_categories():
    return jsonify(list(blueprints.keys()))


if __name__ == "__main__":
    app.run("0.0.0.0", debug=False)
