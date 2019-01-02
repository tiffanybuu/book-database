from flask import Flask, jsonify, request, Response
import json
from settings import *
from BookModel import *


# create a dictionary // not needed bc pulling from database
# books = [
#     {
#         'name': 'Green Eggs and Ham',
#         'price': 7.99,
#         'isbn': 9782828282
#     },
#     {
#         'name': 'The Cat in the Hat',
#         'price': 6.99,
#         'isbn': 9782323222
#
#     }
#
# ]


# Get /store
# app.route binds function to a url
# when someone hits the parameter inside the route function,
@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})


# only add to collection of books if what the user gives us is valid format
def validBookObject(bookObject):
    if "name" in bookObject and "price" in bookObject and "isbn" in bookObject:
        return True
    else:
        return False


# This will allow users themselves to post a book
@app.route('/books', methods=['POST'])
def add_book():
    # get the user inputted information in form of a json object
    request_data = request.get_json()
    if validBookObject(request_data):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        # # if the user decides to add new criteria, filter it out
        # new_book = {
        #     "name": request_data['name'],
        #     "price": request_data['price'],
        #     "isbn": request_data['isbn']
        # }
        # books.insert(0, new_book)
        #201 = status code
        response = Response("", 201, mimetype='application/json')
        # so when you post a response, it leads to a html link with books+isbn
        response.headers['Location'] = "/books" + str(request_data['isbn'])
        return response
    else:
        # Handling invalid post requests
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 978202}",
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype= 'application/json')
        return response


# if someone clicks the url with one of the ISBN for either of the books,
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    # for book in books:
    #     if book["isbn"] == isbn:
    #         return_value = {
    #             'name': book['name'],
    #             'price': book['price']
    #         }
    return jsonify(return_value)


# put route
def valid_put_request_data(request_data):
    if "name" in request_data and "price" in request_data:
        return True
    else:
        return False


@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if not valid_put_request_data(request_data):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 978202}",
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response
    Book.replace_book(isbn, request_data['name'], request_data['price'])
    # new_book = {
    #     'name': request_data['name'],
    #     'price': request_data['price'],
    #     'isbn': isbn
    # }
    # i = 0
    # for book in books:
    #     current_isbn = book['isbn']
    #     if current_isbn == isbn:
    #         books[i] = new_book
    #     i += 1
    response = Response("", status=204)
    return response


# PATCH ROUTE
# Example of a patch is given an isbn, the user wants to change the name of the book name
# Users can also change the price of a book given ISBN
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    #updated_book = {}
    if "name" in request_data:
         # updated_book["name"] = request_data["name"]
        Book.update_book_name(isbn, request_data['name'])
    if "price" in request_data:
        # updated_book["price"] = request_data["price"]
        Book.update_book_price(isbn, request_data['price'])
    # for book in books:
    #     if book["isbn"] == isbn:
    #         book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = '/books/' + str(isbn)
    return response


# DELETE ROUTE
# /books/9782828282

@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
   if Book.delete_book(isbn):
    response = Response("", status=204)
    return response
    invalidBookObjectErrorMsg = {
        "error": "Book with ISBN was not found"
    }

    # i = 0
    # for book in books:
    #     if book["isbn"] == isbn:
    #         books.pop(i)
    #         response = Response("", status=204)
    #         return response
    #     i += 1
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
    return response


app.run(port=5000)
