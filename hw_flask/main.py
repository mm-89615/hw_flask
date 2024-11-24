from flask import jsonify, request
from sqlalchemy import text

from hw_flask.app import app
from hw_flask.utils.db import prepare_db
from hw_flask.utils.http_error import error_handler, HttpError
from hw_flask.utils.middleware import after_request, before_request
from hw_flask.views import AdvertisementView

prepare_db()

app.before_request(before_request)
app.after_request(after_request)

app.register_error_handler(HttpError, error_handler)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/healthcheck')
def healthcheck():
    try:
        # Создаем сессию и выполняем тестовый запрос
        request.session.execute(text('SELECT 1'))  # Тестовый запрос
        return jsonify(
            {"status": "ok", "message": "Database connection is healthy"}
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


advertisement_view = AdvertisementView.as_view('advertisement_view')
app.add_url_rule(
    rule='/ad/',
    view_func=advertisement_view,
    methods=['GET', 'POST']
)
app.add_url_rule(
    rule='/ad/<int:ad_id>',
    view_func=advertisement_view,
    methods=['GET', 'DELETE', 'PATCH']
)

if __name__ == "__main__":

    app.run(host='0.0.0.0')