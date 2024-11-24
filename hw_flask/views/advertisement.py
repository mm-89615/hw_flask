from flask import Flask, jsonify, request
from flask.views import MethodView

from hw_flask.models import Advertisement, Session

app = Flask(__name__)


class AdvertisementView(MethodView):

    def get(self, ad_id: int = None):
        with Session() as session:
            if ad_id is None:
                ads = session.query(Advertisement).all()
                return jsonify([ad.dict for ad in ads])
            ad = session.get(Advertisement, ad_id)
            return jsonify(ad.dict)

    def post(self):
        json_data = request.json
        with Session() as session:
            ad = Advertisement(**json_data)
            session.add(ad)
            session.commit()
            return jsonify(ad.id_dict)

    def patch(self, ad_id: int):
        with Session() as session:
            ad = session.get(Advertisement, ad_id)
            json_data = request.json
            for key, value in json_data.items():
                setattr(ad, key, value)
            session.add(ad)
            session.commit()
            return jsonify(ad.id_dict)

    def delete(self, ad_id: int):
        with Session() as session:
            ad = session.get(Advertisement, ad_id)
            session.delete(ad)
            session.commit()
            return jsonify(ad.id_dict)