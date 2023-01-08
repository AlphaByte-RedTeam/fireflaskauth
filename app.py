import os
import smtplib
import firebase_admin
from os.path import join, dirname
from flask import Flask
from flask_restful import Resource, Api, reqparse
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
    url="https://www.unito.digital/",
    handle_code_in_app=True,
    ios_bundle_id="io.flutter.flutter.app",
    android_package_name="com.example.unito",
    android_install_app=True,
    android_minimum_version="12",
)

email: str = "andrew.avv03@gmail.com"
link: str = auth.generate_sign_in_with_email_link(email, action_code_settings)


@app.route("/")
def get_link() -> str:
    return f"{link}\n"


if __name__ == "__main__":
    app.run(debug=True)
