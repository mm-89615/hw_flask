from flask import Flask, jsonify
from sqlalchemy import text

from hw_flask.models import Session
from hw_flask.views import AdvertisementView

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/healthcheck')
def healthcheck():
    try:
        # Создаем сессию и выполняем тестовый запрос
        with Session() as session:
            session.execute(text('SELECT 1'))  # Тестовый запрос
        return jsonify(
            {"status": "ok", "message": "Database connection is healthy"}
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


advertisement_view = AdvertisementView.as_view('advertisements')
app.add_url_rule(
    rule='/ad/',
    view_func=advertisement_view,
    methods=['POST', 'GET']
)
app.add_url_rule(
    rule='/ad/<int:ad_id>',
    view_func=advertisement_view,
    methods=['GET', 'DELETE', 'PATCH']
)

if __name__ == "__main__":
    app.run(host='0.0.0.0')