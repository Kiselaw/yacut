import random
from urllib.parse import urljoin

from flask import flash, redirect, render_template, request

from . import app, db
from .constants import LENGTH, SYMBOLS
from .forms import URLForm
from .models import URL_map
# тест

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
                    'duplicate-message'
                )
                return render_template('index.html', form=form)
        else:
            short = ''.join(random.choice(SYMBOLS) for _ in range(LENGTH))
            while URL_map.query.filter_by(short=short).first():
                short = ''.join(random.choice(SYMBOLS) for _ in range(LENGTH))
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
    db_object = URL_map.query.filter_by(short=short).first_or_404()
    source = db_object.original
    return redirect(source)
