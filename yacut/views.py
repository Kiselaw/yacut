from . import app, db
from flask import request, render_template, flash, redirect, abort

from .forms import URLForm
from .models import URL_map
from urllib.parse import urljoin
import string
import random
import re

LENGTH = 6


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    base_url = request.base_url
    form = URLForm()
    if form.validate_on_submit():
        if form.custom_id.data:
            short = form.custom_id.data
            if URL_map.query.filter_by(short=short).first():
                flash(
                    f'Имя {short} уже занято!',
                    'error-message'
                )
                return render_template('index.html', form=form)
            if not re.match(r'[a-zA-Z0-9]+$', short):
                flash(
                    'Указано недопустимое имя для короткой ссылки',
                    'error-message'
                )
                return render_template('index.html', form=form)
        else:
            symbols = string.ascii_letters + string.digits
            short = ''.join(random.choice(symbols) for _ in range(LENGTH))
            while URL_map.query.filter_by(short=short).first():
                short = ''.join(random.choice(symbols) for _ in range(LENGTH))
        url = URL_map(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(url)
        db.session.commit()
        flash(f'{urljoin(base_url, short)}', 'success-message')
    return render_template('index.html', form=form)


@app.route('/<string:id>')
def redirect_to_source(id):
    short = id
    db_object = URL_map.query.filter_by(short=short).first()
    if not db_object:
        abort(404)
    source = db_object.original
    return redirect(source)
