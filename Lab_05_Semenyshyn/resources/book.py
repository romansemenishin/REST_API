from flask_restful import Resource, reqparse
from flask_restful import Resource, reqparse

# база даних книг
books_db = {
    1: {"id": 1, "title": "Інтернат", "author": "Сергій Жадан", "status": "наявні", "year": 2017},
    2: {"id": 2, "title": "Я бачу, вас цікавить пітьма", "author": "Ілларіон Павлюк", "status": "видані", "year": 2020},
    3: {"id": 3, "title": "Колонія", "author": "Макс Кідрук", "status": "наявні", "year": 2023},
    4: {"id": 4, "title": "Записки українського самашедшого", "author": "Ліна Костенко", "status": "видані", "year": 2010}
}
book_id_counter = 4

# парсер для обробки вхідних даних
parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help='Назва книги обов\'язкова')
parser.add_argument('author', type=str, required=True, help='Автор обов\'язковий')
parser.add_argument('status', type=str, default="наявні")
parser.add_argument('year', type=int)


class BookList(Resource):
    def get(self):
        """
        Отримати список всіх книг
        ---
        tags:
          - Books
        responses:
          200:
            description: Список усіх книг у бібліотеці
        """
        return list(books_db.values()), 200

    def post(self):
        """
        Додати нову книгу
        ---
        tags:
          - Books
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - title
                - author
              properties:
                title:
                  type: string
                  example: "Танці з кістками"
                author:
                  type: string
                  example: "Андрій Сем'янків"
                status:
                  type: string
                  example: "наявні"
                year:
                  type: integer
                  example: 2022
        responses:
          201:
            description: Книгу успішно створено
        """
        global book_id_counter
        args = parser.parse_args()
        
        book_id_counter += 1
        new_book = {
            "id": book_id_counter,
            "title": args['title'],
            "author": args['author'],
            "status": args['status'],
            "year": args['year']
        }
        books_db[book_id_counter] = new_book
        return new_book, 201


class BookResource(Resource):
    def get(self, book_id):
        """
        Отримати книгу за ID
        ---
        tags:
          - Books
        parameters:
          - in: path
            name: book_id
            type: integer
            required: true
            description: Унікальний ідентифікатор книги
        responses:
          200:
            description: Дані про книгу
          404:
            description: Книгу не знайдено
        """
        if book_id not in books_db:
            return {"message": "Книгу не знайдено"}, 404
        return books_db[book_id], 200

    def delete(self, book_id):
        """
        Видалити книгу
        ---
        tags:
          - Books
        parameters:
          - in: path
            name: book_id
            type: integer
            required: true
            description: Унікальний ідентифікатор книги
        responses:
          204:
            description: Книгу успішно видалено
          404:
            description: Книгу не знайдено
        """
        if book_id not in books_db:
            return {"message": "Книгу не знайдено"}, 404
        
        del books_db[book_id]
        return '', 204