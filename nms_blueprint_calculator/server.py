from flask import Flask, jsonify, render_template, request, session, g, redirect
from json import load
from google.cloud import firestore
from dotenv import load_dotenv
from nms_blueprint_calculator.utils import generate_id
from nms_blueprint_calculator import __version__
import pathlib
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("COOKIE_SIGNING_KEY", generate_id())
db = firestore.Client()
with open(pathlib.Path(__file__).parent.resolve() / "static/blueprints.json", "r") as f:
    base_state = load(f)


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


@app.before_request
def get_or_create_session():
    if "session_id" not in session:
        session["session_id"] = generate_id()
        session_doc = db.collection("sessions").document(session["session_id"])
        session_doc.set({"app_version": __version__, "state": base_state})
        g.blueprints = base_state
    else:
        session_doc = (
            db.collection("sessions").document(session["session_id"]).get().to_dict()
        )
        if not session_doc or session_doc["app_version"] != __version__:
            session.clear()
            return redirect(request.url)
        g.blueprints = session_doc["state"]


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
@app.route("/api/blueprints/<string:category>/")
@app.route("/api/blueprints/", defaults={"category": None})
@app.route("/api/blueprints", defaults={"category": None})
def show_blueprints(category):
    if not category:
        return jsonify(g.blueprints)
    else:
        try:
            return jsonify(g.blueprints[category])
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


@app.route("/api/blueprints/<string:category>/<string:item>", methods=["GET", "PUT"])
def show_item_blueprint(category, item):
    if category not in g.blueprints:
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
    elif item not in g.blueprints[category]:
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
        return jsonify(g.blueprints[category][item])


@app.route("/api/blueprints/categories")
def show_categories():
    return jsonify(list(g.blueprints.keys()))


if __name__ == "__main__":
    app.run("0.0.0.0", debug=False)
