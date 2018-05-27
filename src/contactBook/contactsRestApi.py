from flask import Blueprint, request
from src import basic_auth
from contractOperations import ContractOperations

contractOperations = ContractOperations()

contactBook = Blueprint('contactBook', __name__, url_prefix='/contacts')


@contactBook.route('/', methods=['GET', 'POST'])
@basic_auth.login_required
def test():
    return "test"


@contactBook.route('/add', methods=['POST'])
@basic_auth.login_required
def add_contact():
    """Contact details in body"""
    req_data = request.get_json()
    return contractOperations.c_add(req_data)


@contactBook.route('/edit', methods=['POST'])
@basic_auth.login_required
def edit_contact():
    """email as request param as primary key and edit details in body"""
    email_key = request.args.get('email')
    req_data = request.get_json()
    return contractOperations.c_edit(email_key, req_data)


@contactBook.route('/delete', methods=['GET'])
@basic_auth.login_required
def delete_contact():
    """email as request param as primary key to delete"""
    email_key = request.args.get('email')
    return contractOperations.c_delete(email_key)


@contactBook.route('/search', methods=['POST'])
@basic_auth.login_required
def search():
    """keyword as request param and size and page filter in body defaults to size 10 page 0"""
    keyword = request.args.get('keyword')
    req_data = request.get_json()
    return contractOperations.c_search(keyword, req_data)
