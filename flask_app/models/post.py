from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User
from flask import flash

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.text = data['text']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        self.likes = []
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts JOIN users ON users.id = posts.user_id;"
        results = connectToMySQL('theolobate').query_db(query)
        posts = []
        for post in results:
            instance = cls(post)
            userinfo = {
                "id" : post['users.id'],
                "first_name" : post['first_name'],
                "last_name" : post['last_name'],
                "email" : post['email'],
                "password" : post['password'],
                "created_at" : post['users.created_at'],
                "updated_at" : post['users.updated_at']
            }
            instance.user = User(userinfo)
            posts.append(instance)
        return posts
    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['text']) < 1:
            flash("Text field required.")
            is_valid = False
        return is_valid
    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (text, created_at, updated_at, user_id) VALUES(%(text)s, NOW(), NOW(), %(user_id)s);"
        post_id = connectToMySQL('theolobate').query_db(query,data)
        return post_id
    @classmethod
    def get(cls, data):
        query = "SELECT * FROM posts JOIN users ON users.id = posts.user_id WHERE posts.id = %(id)s;"
        result = connectToMySQL('theolobate').query_db(query, data)
        post = result[0]
        instance = cls(post)
        userinfo = {
            "id" : post['users.id'],
            "first_name" : post['first_name'],
            "last_name" : post['last_name'],
            "email" : post['email'],
            "password" : post['password'],
            "created_at" : post['users.created_at'],
            "updated_at" : post['users.updated_at']
        }
        instance.user = User(userinfo)
        return instance
    @classmethod
    def remove(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        connectToMySQL('theolobate').query_db(query, data)
        return
    @classmethod
    def update(cls, data):
        query = "UPDATE posts SET text = %(text)s, updated_at = NOW() WHERE id = %(id)s;"
        post = connectToMySQL('theolobate').query_db(query,data)
        return post