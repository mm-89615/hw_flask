from typing import Optional

from pydantic import BaseModel, ValidationError

from hw_flask.utils.http_error import HttpError


class CreateAdvertisementSchema(BaseModel):
    title: str
    description: Optional[str]
    owner: str


class UpdateAdvertisementSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    owner: Optional[str]


def validate_json(json_data, schema_cls):
    try:
        schema_obj = schema_cls(**json_data)
        json_data_validated = schema_obj.dict(exclude_unset=True)
        return json_data_validated
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop("ctx", None)
        raise HttpError(status_code=400, message=errors)