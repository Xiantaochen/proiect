
from app.libs.redprint import Redprint

api = Redprint('test')

@api.route('', methods=['GET'])
def get_book():
    return 'get book'


@api.route('', methods=['POST'])
def create():
    return 'create book'
