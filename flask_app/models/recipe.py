
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
from flask_app.models import user
from datetime import date
bcrypt = Bcrypt(app)
# The above is used when we do login registration, be sure to install flask-bcrypt: pipenv install flask-bcrypt


class Recipe:
    db = "recipes_db" #which database are you using for this project
    def __init__(self, data):
        if 'recipes.user_id' in data:
            self.id = data['recipes.id']
            self.user_id = data['recipes.user_id']
            self.name = data['name']
            self.description = data['description']
            self.instructions = data['instructions']
            self.date_made = data['date_made']
            self.under_30 = data['under_30']
            self.created_at = data['recipes.created_at']
            self.updated_at = data['recipes.updated_at'] 
        elif 'recipes.id' in data:
            self.id = data['recipes.id']
            self.user_id = data['user_id']
            self.name = data['name']
            self.description = data['description']
            self.instructions = data['instructions']
            self.date_made = data['date_made']
            self.under_30 = data['under_30']
            self.created_at = data['recipes.created_at']
            self.updated_at = data['recipes.updated_at']
        else:
            self.id = data['id']
            self.user_id = data['user_id']
            self.name = data['name']
            self.description = data['description']
            self.instructions = data['instructions']
            self.date_made = data['date_made']
            self.under_30 = data['under_30']
            self.created_at = data['created_at']
            self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added her for class association?
        self.creator = None
        self.user_favorites = []
        self.num_of_favorites = data.get('favorites_count', 0)


    # Create Recipes Models
    @classmethod
    def create_recipe(cls, recipe_data):
        if not Recipe.validate_recipe_data(recipe_data):
            return False
        query = """
        INSERT INTO recipes (user_id, name, description, instructions, date_made, under_30)
        VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s)
        ;"""
        recipe_id = connectToMySQL(cls.db).query_db(query, recipe_data)
        return recipe_id


    # Read Recipes Models
    @classmethod
    def get_recipe_by_id(cls, recipe_id):
        data = {'id':recipe_id}
        query = """
        SELECT * FROM recipes
        WHERE id = %(id)s
        ;"""
        recipes_list = connectToMySQL(cls.db).query_db(query, data)
        return cls(recipes_list[0])

    @classmethod
    def get_all_recipes_with_users(cls, order_by="name", sort_by="ASC"):
        order_by = Recipe.change_order_by(order_by)
        sort_by = Recipe.validate_sort_query(sort_by)
        data = {
            'order':order_by,
            'sort' : sort_by
        }
        query = f"""
        SELECT *,
        (
        SELECT COUNT(favorites.recipe_id) from favorites
        WHERE recipes.id = favorites.recipe_id 
        ) AS favorites_count
        FROM recipes
        JOIN users 
        ON recipes.user_id = users.id
        ORDER BY {data['order']} {data['sort']}
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for row in results:
            this_recipe = cls(row)
            this_recipe.creator = user.User(row)
            recipes.append(this_recipe)
        return recipes
    
    @classmethod
    def get_recipe_by_id_with_user(cls, recipe_id):
        data = {'id':recipe_id}
        query = """
        SELECT * FROM recipes
        JOIN users
        ON recipes.user_id = users.id
        WHERE recipes.id = %(id)s
        ;"""
        result_list = connectToMySQL(cls.db).query_db(query,data)
        this_recipe = cls(result_list[0])
        this_recipe.creator = user.User(result_list[0])
        return this_recipe

    @classmethod
    def show_top_recipes_by_favorites(cls):
        query = """
        SELECT *,
        (
        SELECT COUNT(*) FROM favorites 
        WHERE favorites.recipe_id = recipes.id
        ) AS favorites_count
        FROM recipes
        ORDER BY favorites_count DESC
        LIMIT 5;
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        top_five_recipes = []
        for row in results:
            top_five_recipes.append(cls(row))
        return top_five_recipes
    
    @classmethod
    def get_3_random_recipe_with_favorites(cls):
        query = """
        SELECT recipes.*, users.*,
        (
            SELECT COUNT(*) FROM favorites
            WHERE favorites.recipe_id = recipes.id
        ) AS favorite_count
        FROM recipes
        JOIN users ON recipes.user_id = users.id
        ORDER BY RAND()
        LIMIT 3
        ;"""
        result_list = connectToMySQL(cls.db).query_db(query)
        if result_list:
            random_recipes = []
            for row in result_list:
                this_recipe = cls(row)
                this_recipe.creator = user.User(row)
                random_recipes.append(this_recipe)
            return random_recipes
        return False

    # Update Recipes Models
    @classmethod
    def update_recipe(cls, recipe_data):
        if not Recipe.validate_recipe_data(recipe_data):
            return False
        query = """
        UPDATE recipes
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s
        WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query,recipe_data)
        return True




    # Delete Recipes Models
    @classmethod
    def delete_recipe(cls, recipe_id):
        query = """
        DELETE FROM recipes
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query,{'id': recipe_id})
        

    #Validations
    @staticmethod
    def validate_recipe_data(data):
        is_valid = True
        print(len(data['name']),len(data['description']), len(data['instructions'])  )
        if len(data['name']) <= 0 or len(data['description']) <= 0 or len(data['instructions']) <= 0:
            flash("Please fill out all recipe info fields")
            is_valid = False
        #validate date vs current date
        if data['date_made'] != '':
            date_made = date.fromisoformat(data['date_made'])
            current_date = date.today()
            if date_made > current_date:
                flash("You may think you're from the future but you're not! Date made must be today or in the past.")
                is_valid = False
        else:
            flash("Please select a date made")
            is_valid = False
        if 'under_30' not in data:
            flash('Select if recipe is under 30 minutes or not')
            is_valid = False
        return is_valid
    
    @staticmethod
    def change_order_by(order_by):
        
        columns = {
            'cb' : 'first_name',
            '30' : 'under_30',
            'fav' : 'favorites_count',
            'n' : 'name'
        }
        if order_by not in columns: return 'name'
        return columns[order_by]


    @staticmethod
    def validate_sort_query(sort):
        if sort.lower() == 'asc': return 'asc'
        else: return 'desc'

    #Format Time
    @staticmethod
    def formate_date_time(created_at):
        day = int(created_at.strftime("%d"))
        formatted_date = created_at.strftime("%B") + " " + str(day) + created_at.strftime(", %Y")
        return formatted_date