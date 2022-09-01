import random
import re
import string
from urllib.parse import urljoin

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map


LENGTH = 6


@app.route('/api/id/<string:id>/', methods=['GET'])
def get_original_link(id):
    db_object = URL_map.query.filter_by(short=id).first()
    if db_object is None:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            404
        )
    return jsonify({'url': db_object.original}), 200


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    base_url = request.url_root
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    elif 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    elif (
        (
            'custom_id' in data and
            data['custom_id'] is not None
        ) and
        (
            len(data['custom_id']) > 16 or not
            re.match(r'^$|^[a-zA-Z0-9]+$', data['custom_id'])
        )
    ):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    elif (
        'custom_id' in data and
        URL_map.query.filter_by(short=data['custom_id']).first() is not None
    ):
        raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
    elif (
        'custom_id' in data and
        data['custom_id'] is not None and
        len(data['custom_id']) > 0
    ):
        short = data['custom_id']
    else:
        symbols = string.ascii_letters + string.digits
        short = ''.join(random.choice(symbols) for _ in range(LENGTH))
        while URL_map.query.filter_by(short=short).first():
            short = ''.join(random.choice(symbols) for _ in range(LENGTH))
    url = URL_map(
        original=data['url'],
        short=short,
    )
    db.session.add(url)
    db.session.commit()
    return jsonify(
        {
            'short_link': urljoin(base_url, short),
            'url': data['url']
        }
    ), 201
