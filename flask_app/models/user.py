
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, be sure to install flask-bcrypt: pipenv install flask-bcrypt


class User:
    db = "recipes_db" #which database are you using for this project
    def __init__(self, data):
        if 'users.id' in data:
            self.id = data['users.id']
            self.first_name = data['first_name']
            self.last_name = data['last_name']
            self.email = data['email']
            self.password = data['password']
            self.created_at = data['users.created_at']
            self.updated_at = data['users.updated_at']
        else:
            self.id = data['id']
            self.first_name = data['first_name']
            self.last_name = data['last_name']
            self.email = data['email']
            self.password = data['password']
            self.created_at = data['created_at']
            self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added her for class association?
        self.recipes = []
        self.recipe_favorites = []


    # Create Users Models
    @classmethod
    def create_user(cls, user_data):
        if not cls.validate_user_data(user_data):
            return False
        # user_data = cls.parse_registration_data(user_data)
        user_data = user_data.copy()
        user_data['password'] = bcrypt.generate_password_hash(user_data['password'])
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""

        user_id = connectToMySQL(cls.db).query_db(query, user_data)
        session['user_id'] = user_id
        session['first_name'] = user_data['first_name']
        return user_id


    # Read Users Models
    @classmethod
    def get_user_by_email(cls, email):
        data = {'email': email}
        query = """
        SELECT * FROM users
        WHERE email = %(email)s
        ;"""
        users_list = connectToMySQL(cls.db).query_db(query, data)
        if users_list:
            return cls(users_list[0])
        return False

    # Update Users Models



    # Delete Users Models

    #Validations
    @staticmethod
    def validate_user_data(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[\W_]).+$')
        is_valid = True
        if len(data['first_name']) < 2 or len(data['last_name']) < 2:
            flash("Come on silly, your name must be more than 1 character!")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address. Please enter a valid email.")
            is_valid = False
        if User.get_user_by_email(data['email'].lower().strip()):
            is_valid = False
            flash('Nice try! That email is already in use...')
        if not PASSWORD_REGEX.match(data['password']):
            flash("Password requires at least 1 number and special character")
            is_valid = False
        if len(data['password']) < 8:
            flash('Your password must be at least 8 character')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Passwords did not match. No matchy no worky!')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(user_data):
        if 'password_attempts' in session and session['password_attempts'] <= 0:
            flash('You have no attempts left! You must wait 30 minutes to try again')
            return False
        this_user = User.get_user_by_email(user_data['email'].lower().strip())
        if this_user:
            if bcrypt.check_password_hash(this_user.password, user_data['password']):  
                session['user_id'] = this_user.id
                session['first_name'] = this_user.first_name
                return True
        #login failed, take away login attempts
        if 'password_attempts' not in session:
            session['password_attempts'] = 5
        else:
            session['password_attempts'] -= 1
        flash(f"Incorrect login. You have {session['password_attempts']} more attempts!")
        return False




    @staticmethod
    def parse_registration_data(user_data):
        parsed_user_data = {}
        parsed_user_data['first_name'] = user_data['first_name']
        parsed_user_data['last_name'] = user_data['last_name']
        parsed_user_data['email'] = user_data['email'].lower().strip()
        parsed_user_data['password'] =  bcrypt.generate_password_hash(user_data['password'])
        return parsed_user_data
    
