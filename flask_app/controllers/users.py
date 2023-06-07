from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user # import entire file, rather than class, to avoid circular imports

# Create Users Controller
@app.route('/user/login/registraion', methods=['POST'])
def user_login_registration():
    print(request.form)
    return redirect('/recipes')


# Read Users Controller

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/recipes')
def profile_page():
    return render_template('recipes.html')

@app.route('/recipes/new')
def show_new_recipes_page():
    return render_template('new_recipe.html')

@app.route('/recipes/<int:recipe_id>')
def show_one_recipe(recipe_id):
    return render_template('show_recipe.html')

@app.route('/recipes/edit/<int:recipe_id>')
def update_recipe_page(recipe_id):
    return render_template('edit_recipe.html')



# Update Users Controller



# Delete Users Controller


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