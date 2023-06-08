from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user # import entire file, rather than class, to avoid circular imports

# Create Users Controller
@app.route('/user/login_reg', methods=['POST'])
def user_login_registration():
    if request.form['which_form'] == 'registration_form':
        if user.User.create_user(request.form):
            return redirect('/recipes')
        registration_info = {
            'first_name': request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email']
        }
        return render_template('home.html', registration_info = registration_info)
    if user.User.validate_login(request.form):
        return redirect('/recipes')
    return render_template('home.html', login_email = request.form['email'], registration_info = None)


# Read Users Controller

@app.route('/user/logout')
def user_logout():
    session.clear()
    return redirect('/')


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