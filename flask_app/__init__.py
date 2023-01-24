# import flask from Flask
from flask import Flask, render_template, request, redirect, session, flash
# import Bcrype to hash/encode password
from flask_bcrypt import Bcrypt  


app = Flask(__name__)
app.secret_key = "sapientia et doctrina : wisdom and learning"

bcrypt = Bcrypt(app)
