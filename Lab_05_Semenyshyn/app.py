from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from resources.book import BookList, BookResource

app = Flask(__name__)
api = Api(app)

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Лабораторна робота №5 - Семенишин Роман",
        "description": "Flask-RESTful та Flasgger",
        "version": "1.0.0"
    }
}

# Flasgger автоматично налаштує всі системні маршрути та відкриє UI за адресою /apidocs/
swagger = Swagger(app, template=swagger_template)

# реєстрація маршрутів
api.add_resource(BookList, '/books')
api.add_resource(BookResource, '/books/<int:book_id>')

if __name__ == '__main__':
    app.run(debug=True, port=8000)