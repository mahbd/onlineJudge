import os, sys

# edit your username below
sys.path.append("/home/mahbd/public_html/judge")

sys.path.insert(0, os.path.dirname(__file__))
from app import app as application

# make the secret code a little better
application.secret_key = 'secret'