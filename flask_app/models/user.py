from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import MyCustomDB
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')

class User:                         # singular instance of...
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



    @staticmethod
    def validate_register(data):
        is_valid = True

        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(MyCustomDB).query_db(query, data)
        if len(results) >= 1:
            flash('email already in use', 'register')
            is_valid = False

        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(data['email']): 
            flash('Invalid email address!', 'register')
            is_valid = False

        if len(data['first_name']) < 2 or len(data['last_name']) < 2:
            flash('name too short', 'register')
            is_valid = False

        if not NAME_REGEX.match(data['first_name']) or not NAME_REGEX.match(data['last_name']):
            flash('Name must be only letters', 'register')
            is_valid = False

        if len(data['password']) < 8:
            flash('password must be longer than 8 characters', 'register')
            is_valid = False

        if not data['password'] == data['confirm_password']:
            flash('passwords must match', 'register')
            is_valid = False


        return is_valid




    @staticmethod
    def validate_login(data):
        is_valid = True

        for row in User.get_all():
            if not data['email'] in row.email or not data['password'] in row.password:
                flash("email/password incorrect", 'login')
                is_valid = False
        
        return is_valid




    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
    # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(MyCustomDB).query_db(query)
    # Create an empty list to append our instances of users
        my_users = []
    # Iterate over the db results and create instances of users with cls.
        for row in results:
            my_users.append( cls(row) )
        print('from the get all method')
        return my_users


    @classmethod
    def save(cls, data):

        query = "INSERT INTO users ( first_name , last_name, email , password , created_at , updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s , NOW() , NOW() );"

        return connectToMySQL(MyCustomDB).query_db( query, data )


    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(MyCustomDB).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])