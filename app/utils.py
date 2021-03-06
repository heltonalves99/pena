import string
import random
from math import ceil

from bottle import request, response, parse_auth
from passlib.hash import sha256_crypt

from app.settings import PAGINATE_BY
from app.models.users import User
from app.models import db


def authenticated(func):
    def wrapper(*args, **kwargs):
        check = check_pass()
        if check[0]:
            return func(check[1], *args, **kwargs)
        response.status = 401
        return {'status': 'error', 'message': 'Error with auth data provided.'}
    return wrapper


def check_pass():
    auth = request.headers.get('Authorization')

    if not auth:
        return False

    username, password = parse_auth(auth)
    user = db.query(User).filter(User.username == username).first()
    return sha256_crypt.verify(password, user.password), user


def check_exist(model, key, value):
    obj = db.query(model).filter(key == value).first()
    if obj:
        return obj
    return None


def generate_token(size=20, chars=string.ascii_uppercase + string.digits):
    """
        from: http://stackoverflow.com/a/2257449/492161
    """
    return ''.join(random.choice(chars) for _ in range(size))


def paginate(query, page=1, paginate_by=PAGINATE_BY):
    count = query.count()
    qtd_pages = int(ceil(count / paginate_by))

    prev = (page - 1) if page > 1 else None
    next = (page + 1) if page < qtd_pages else None
    start = (page - 1) * paginate_by
    end = start + paginate_by

    pagination = {
        'pagination': {
            'page': page,
            'prev': prev,
            'next': next
        },
        'results': query[start:end]
    }

    return pagination
