
# import dunder init __init__ to get app module
from flask_app import app
#import users.py in controllers folder
from flask_app.controllers import users, recipes


if __name__ == '__main__':
    app.run(debug=True)