from flask_app import app, render_template, redirect, request, bcrypt, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from pprint import pprint

@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('recipes.html', allrecipes = Recipe.get_all_recipe_info())

# Add new Recipes
#route to handle the form
@app.route("/recipes/new")
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("addrecipes.html")

# route to handle the data on the form
@app.route("/recipes/create", methods=['POST'])
def add_new_recipe():
    print(request.form)    
    # validate our recipe
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    pprint (request.form)
    Recipe.create_new_recipe(request.form)
    return redirect('/recipes')

## view recipe 
@app.route("/recipes/<int:id>")
def displayrecipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id':id}  # create an id dictionary with the content of id (from <int:id>)
    return render_template("displayrecipe.html", recipe=Recipe.get_one_recipe(data))

# route to edit recipe
@app.route("/recipes/edit/<int:id>")
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id':id}
    # pprint (Recipe.get_one_recipe(data))
    return render_template("editrecipes.html", recipe=Recipe.get_one_recipe(data))

@app.route("/recipes/edit_recipe", methods=['POST'])
def edit_a_recipe():
    pprint (request.form)
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/recipes/edit/{request.form['id']}")
    Recipe.updaterecipe(request.form)
    return redirect('/recipes')

# delete recipe
@app.route("/recipes/delete/<int:id>")
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    Recipe.delete_recipe(data = {'id':id})
    return redirect('/recipes')