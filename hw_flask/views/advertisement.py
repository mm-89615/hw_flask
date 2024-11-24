from flask import jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from hw_flask.models import Advertisement
from hw_flask.utils.http_error import HttpError
from hw_flask.utils.validation import (
    CreateAdvertisementSchema,
    UpdateAdvertisementSchema, validate_json
)


def get_ad_by_id(ad_id: int) -> Advertisement | None:
    ad = request.session.get(Advertisement, ad_id)
    if not ad:
        raise HttpError(status_code=404, message="Advertisement not found")
    return ad


def get_ads():
    ads = request.session.query(Advertisement).all()
    if not ads:
        raise HttpError(status_code=404, message="Advertisements not found")
    return ads


def add_ad(ad: Advertisement):
    request.session.add(ad)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(status_code=409, message="Advertisement already exists")


class AdvertisementView(MethodView):

    def get(self, ad_id: int = None):
        if ad_id is None:
            ads = get_ads()
            return jsonify([ad.dict for ad in ads])
        ad = get_ad_by_id(ad_id)
        return jsonify(ad.dict)

    def post(self):

        json_data = validate_json(request.json, CreateAdvertisementSchema)
        ad = Advertisement(**json_data)
        add_ad(ad)
        return jsonify(ad.id_dict)

    def patch(self, ad_id: int):
        ad = get_ad_by_id(ad_id)
        json_data = validate_json(request.json, UpdateAdvertisementSchema)
        for key, value in json_data.items():
            setattr(ad, key, value)
        add_ad(ad)
        return jsonify(ad.id_dict)

    def delete(self, ad_id: int):
        ad = get_ad_by_id(ad_id)
        request.session.delete(ad)
        request.session.commit()
        return jsonify(ad.id_dict)