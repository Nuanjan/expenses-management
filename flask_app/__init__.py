from flask import Flask
app = Flask(__name__)
import os
from dotenv import load_dotenv

app.secret_key = os.getenv('SECRET_KEY')
