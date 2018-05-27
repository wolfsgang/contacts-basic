from flask import Blueprint, request
from src import basic_auth
from contractOperations import ContractOperations
contractOperations = ContractOperations()

contactBook = Blueprint('contactBook', __name__, url_prefix='/contacts')


@contactBook.route('/', methods=['GET', 'POST'])
@basic_auth.login_required
def test():
    return "test"


@basic_auth.login_required
@contactBook.route('/add', methods=['POST'])
def add_contact():
    req_data = request.get_json()
    return contractOperations.addContact(req_data)


@basic_auth.login_required
@contactBook.route('/edit', methods=['POST'])
def edit_contact():
    email_key = request.args.get('email')
    req_data = request.get_json()
    return contractOperations.editContact(email_key, req_data)


@basic_auth.login_required
@contactBook.route('/delete', methods=['DELETE'])
def delete_contact():
    email_key = request.args.get('email')
    return contractOperations.deleteContact(email_key)


@basic_auth.login_required
@contactBook.route('/search', methods=['POST'])
def search():
    email_key = request.args.get('emailId')
    name = request.args.get('name')
    req_data = request.get_json()
    return contractOperations.searchContact(email_key, name, req_data)


