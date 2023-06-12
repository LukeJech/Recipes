from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, recipe # import entire file, rather than class, to avoid circular imports
import random

# Create Recipe Controller
@app.route('/recipes/new', methods=['POST', 'GET'])
def show_new_recipes_page():
    if 'user_id' not in session: return redirect('/')
    if request.method == 'GET':
        return render_template('new_recipe.html')
    #validate recipe, create if valid, redirect to recipes page
    print(request.form)
    if recipe.Recipe.create_recipe(request.form):
        return redirect('/recipes')
    return render_template('new_recipe.html', recipe_info = request.form)


# Read Recipe Controller
@app.route('/')
def home_page():
    return render_template('home.html', random_recipe = recipe.Recipe.get_one_random_recipe_with_favorites() ,registration_info = None, login_email = '')

@app.route('/recipes')
def profile_page():
    if 'user_id' not in session: return redirect('/')
    return render_template('recipes.html', top_recipes = recipe.Recipe.show_top_recipes_by_favorites())



@app.route('/recipes/<int:recipe_id>')
def show_one_recipe(recipe_id):
    if 'user_id' not in session: return redirect('/')
    this_recipe = recipe.Recipe.get_recipe_by_id_with_user(recipe_id)
    this_recipe.date_made = recipe.Recipe.formate_date_time(this_recipe.date_made)
    return render_template('show_recipe.html', recipe = this_recipe )



@app.route('/recipes/all', defaults={'order': 'name', 'sort': 'asc'})
@app.route('/recipes/all/<order>/<sort>')
def show_all_recipes(order, sort):
    if 'user_id' not in session: return redirect('/')
    return render_template('all_recipes.html', all_recipes = recipe.Recipe.get_all_recipes_with_users(order, sort), sort = 'asc')


# Update Users Controller
@app.route('/recipes/edit/<int:recipe_id>', methods=['POST', 'GET'])
def update_recipe_page(recipe_id):
    if 'user_id' not in session: return redirect('/')
    if request.method == 'GET':
        return render_template('edit_recipe.html', recipe = recipe.Recipe.get_recipe_by_id(recipe_id))
    if recipe.Recipe.update_recipe(request.form):
        return redirect(f'/recipes/{recipe_id}')
    return redirect(f'/recipes/edit/{recipe_id}')



# Delete Users Controller
@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    if 'user_id' not in session: return redirect('/')
    recipe.Recipe.delete_recipe(recipe_id)
    return redirect('/recipes')


# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')
# def index(id):
#     user_info = user.User.get_user_by_id(id)
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.