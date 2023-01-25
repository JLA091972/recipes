###################################
## should contain only *methodsd ##
###################################

# import mysqlconnection, and pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from pprint import pprint

# import the regex module "re"
import re

# create a regular expression object to check to validate email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

#define Database name
DATABASE = 'recipes'

# model the User class after the user table from our database
# define from db table object
class User:
    def __init__( self , data ) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # Read DB
    # Now we use class methods to query our database
    @classmethod
    def get_all_user(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        # pprint(results)
        # Create an empty list to append our instances of users
        users = []
        # Iterate over the db results and create instances of users with cls.
        for user in results:
            users.append( cls(user) )
        return users

    ## add new user to db
    @classmethod
    def create_new_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        print ("!!!!!!!!!!!",query)
        return connectToMySQL(DATABASE).query_db(query, data)

    # check and verify, query db if email entered in the login form exists in db
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        # print(result)
        if len(result) > 0:
            return User(result[0])
        else:
            return False


    # Validation steps
    @staticmethod
    def validate_user(user:dict) -> bool:
        is_valid = True
        
        # check if first name is at least 2 char
        if len(user['first_name']) < 2:
            is_valid = False
            flash("First name must be at least 2 characters")

        # check if last name is at least 2 char
        if len(user['last_name']) < 2:
            is_valid = False
            flash("Last name must be at least 2 characters")        
        
        #check if password matches with confirm password
        if user['password'] != user['confirm-password']:
            is_valid = False
            flash("passwords do not match")

        # use regex to check if email is valid
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False

        # check length of password is at least 8 chars in lenght
        if len(user['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters")






        # return value of is_valid
        return is_valid
