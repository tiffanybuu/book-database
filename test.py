def validBookObject(bookObject):
    if "name" in bookObject and "price" in bookObject and "isbn" in bookObject:
        return True
    else:
        return False


valid_object = {
    'name': 'F',
    'price': 6.99,
    'isbn': 1234567890
}

missing_name = {
    'price': 6.99,
    'isbn': 1234567890
}


missing_name = {
    'name': 'F',
    'isbn': 1234567890
}

missing_identity = {
    'name': 'F',
    'isbn': 1234567890
}

empty_dictionary = {}
