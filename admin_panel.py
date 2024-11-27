from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///admin.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    is_blocked = db.Column(db.Boolean, default=False)

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "is_blocked": user.is_blocked} for user in users])

@app.route("/block_user", methods=["POST"])
def block_user():
    data = request.json
    user = User.query.filter_by(id=data["id"]).first()
    if user:
        user.is_blocked = True
        db.session.commit()
        return jsonify({"message": "User blocked successfully"}), 200
    return jsonify({"message": "User not found"}), 404

@app.route("/update_api_key", methods=["POST"])
def update_api_key():
    global WEATHER_API_KEY
    data = request.json
    WEATHER_API_KEY = data["api_key"]
    return jsonify({"message": "API key updated successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
