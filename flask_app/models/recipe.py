#################################
## should contain only methods ##
#################################

# import mysqlconnection, and pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from pprint import pprint

# import the regex module "re"
import re

#define Database name
DATABASE = 'recipes'

# model the Recipe class after the recipe table from our database
# define from db table object
class Recipe:
    def __init__( self , data ) -> None:
        self.id = data['id']
        self.recipe_name = data['recipe_name']
        self.recipe_description = data['recipe_description']
        self.recipe_instructions = data['recipe_instructions']
        self.cooked_date = data['cooked_date']
        self.under_30mins = data['under_30mins']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
    
    # Read DB
    # Now we use class methods to query our database
    @classmethod
    def get_all_recipe(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(DATABASE).query_db(query)
        # pprint(results)
        # Create an empty list to append our instances of recipes
        recipes = []
        # Iterate over the db results and create instances of recipes with cls.
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes

    ## add new recipe to db
    @classmethod
    def create_new_recipe(cls, data):
        query = "INSERT INTO recipes (recipe_name, recipe_description, recipe_instructions, cooked_date, under_30mins, user_id) VALUES (%(recipe_name)s, %(recipe_description)s, %(recipe_instructions)s, %(cooked_date)s,%(under_30mins)s, %(user_id)s);"
        connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_recipe_info(cls):
        query = "SELECT * FROM recipes JOIN users on recipes.user_id = users.id "
        recipe_list = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        # Iterate over the db results and create instances of recipes with cls.
        for recipe in recipe_list:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes JOIN users on users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)  
        pprint(result)
        return Recipe(result[0])

    @classmethod
    def updaterecipe(cls, data):
        print(data)
        query = "UPDATE recipes SET recipe_name=%(recipe_name)s, recipe_description=%(recipe_description)s, recipe_instructions=%(recipe_instructions)s, cooked_date= %(cooked_date)s, under_30mins=%(under_30mins)s where id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)  

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data) 

    # Validation steps
    @staticmethod
    def validate_recipe(recipe:dict) -> bool:
        is_valid = True

        # check if recipe name is at least 3 char
        if len(recipe['recipe_name']) < 3:
            is_valid = False
            flash("Recipe name must be at least 3 characters")

        # check if recipe description is at least 2 char
        if len(recipe['recipe_description']) < 3:
            is_valid = False
            flash("Recipe description must be at least 3 characters")
        
        # check if recipe instructions is at least 3 char
        if len(recipe['recipe_instructions']) < 3:
            is_valid = False
            flash("Recipe instructions must be at least 3 characters")

        # check if recipe cooked date is filled in
        if len(recipe['cooked_date']) < 1:
            is_valid = False
            flash("Cooked Date must be filled")

        # check if recipe cooked date is filled in
        if not "under_30mins" in recipe:
            is_valid = False
            flash("Cook Time 'Under 30 mins' must be filled")
        
        #return value of is_valid        
        return is_valid
