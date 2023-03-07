from flask import Flask, jsonify
from flask_restful import Api, Resource, abort, reqparse
from werkzeug.exceptions import HTTPException, BadRequest, NotFound, InternalServerError

app = Flask(__name__)
api = Api(app)

# Create a parser for POST requests
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name is required')
parser.add_argument('age', type=int, required=True, help='Age is required')

# Define a list of items for demonstration purposes
items = [
    {'id': 1, 'name': 'John', 'age': 25},
    {'id': 2, 'name': 'Jane', 'age': 30},
    {'id': 3, 'name': 'Bob', 'age': 35}
]

# Define a function to find an item by ID
def find_item_by_id(item_id):
    for item in items:
        if item['id'] == item_id:
            return item
    return None

# Define a resource for getting and deleting items by ID
class Item(Resource):
    def get(self, item_id):
        item = find_item_by_id(item_id)
        if not item:
            raise NotFound(f'Item with ID {item_id} not found')
        return item
    
    def delete(self, item_id):
        item = find_item_by_id(item_id)
        if not item:
            raise NotFound(f'Item with ID {item_id} not found')
        items.remove(item)
        return '', 204

# Define a resource for getting all items and adding new ones
class Items(Resource):
    def get(self):
        return items
    
    def post(self):
        args = parser.parse_args()
        item = {'id': len(items) + 1, 'name': args['name'], 'age': args['age']}
        items.append(item)
        return item, 201

# Add the resources to the API
api.add_resource(Item, '/item/<int:item_id>')
api.add_resource(Items, '/items')

# Define a handler for all HTTP exceptions
@app.errorhandler(HTTPException)
def handle_http_exception(error):
    response = jsonify({'message': error.description})
    response.status_code = error.code
    return response

# Define a handler for other exceptions
@app.errorhandler(Exception)
def handle_exception(error):
    if isinstance(error, BadRequest):
        message = 'Invalid request data'
        code = error.code
    else:
        message = 'Internal Server Error'
        code = 500
    response = jsonify({'message': message})
    response.status_code = code
    return response

# Define the menu
menu = '''
 ____ ____ ____ ____ ____ ____ ____ 
||A |||P |||I |||- |||E |||r |||r |||
||__|||__|||__|||__|||__|||__|||__|||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|
by Tadashi10

1. List all items
2. Add new item
3. Get item by ID
4. Delete item by ID
5. Quit
'''

# Print the menu and get user input
while True:
    print(menu)
    choice = input('Enter your choice: ')

    # List all items
    if choice == '1':
        print('All items:')
        print(items)
        input('Press Enter to continue...')

    # Add new item
    elif choice == '2
