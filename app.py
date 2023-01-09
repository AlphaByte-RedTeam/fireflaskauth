import os
import re
import smtplib
import firebase_admin
from flask import Flask, request, jsonify
from markupsafe import escape
from flask_restful import Api
from firebase_admin import auth, credentials
from dotenv import load_dotenv

app = Flask(__name__)
api = Api(app)

# Check if Firebase App is already initialize
if not firebase_admin._apps:
    # Initialize Firebase App
    cred: credentials = credentials.Certificate(
        "serviceAccountKey.json"
    )  # Add your serviceAccountKey.json
    default_app = firebase_admin.initialize_app(cred)

DOTENV_PATH = "secrets.env"
load_dotenv(DOTENV_PATH)

SMTP_SERVER_NAME: str = "smtp.mailersend.net"
SMTP_PORT: int = 587
smtp = smtplib.SMTP(SMTP_SERVER_NAME, SMTP_PORT)
smtp.starttls()
smtp.login(
    os.getenv("SMTP_USERNAME"),
    os.getenv("SMTP_PASSWORD"),
)

action_code_settings = auth.ActionCodeSettings(
    url="https://www.unito.digital/auth/successful",
    handle_code_in_app=True,
    ios_bundle_id="io.flutter.flutter.app",
    android_package_name="com.example.unito",
    android_install_app=True,
    android_minimum_version="12",
)


@app.route("/")
def hello():
    return "Hello, world"


@app.route("/link", methods=["GET"])
def generate_link():
    # Validate the request body
    email = request.args.get("email")
    if not email or not re.match(
        r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email
    ):
        return "Invalid email", 400
    try:
        link = auth.generate_sign_in_with_email_link(email, action_code_settings)
    except Exception as e:
        return f"Error generating link: {e}", 500
    return jsonify({"link": link})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

smtp.close()
