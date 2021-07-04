from bson import ObjectId
from flask import request
from marshmallow import Schema, fields

from src.commons.exception import ValidationError

default_error_messages = {
    'null': 'Bu alan null olamaz.',
    'required': 'Bu alan gereklidir.',
    'validator_failed': 'Doğrulanamayan değer.'
}

default_error_messages_en = {
    'null': 'Field may not be null.',
    'required': 'Missing data for required field.',
    'validator_failed': 'Invalid value.'
}

# default_error_messages=default_error_messages,

# Schema.TYPE_MAPPING[ObjectId] = fields.String

Schema.TYPE_MAPPING[ObjectId] = fields.Str
Schema.TYPE_MAPPING[ObjectId] = fields.String


class BaseSchema(Schema):

    def __init__(self, many: bool = False, *args, **kwargs):
        kwargs["many"] = many
        kwargs["strict"] = True
        super().__init__(*args, **kwargs)

    def convert_from_schema(self, schema):
        return self.deserialize(schema)

    def deserialize(self, payload):
        """
        - Objeyi validasyon'dan geçirir ve eğer valid olmuyorsa exception atar
        - Şemadan şemaya dönüştürme yapmak için de kullanılır.
        :param payload:
        :return:
        """
        result = self.load(payload)
        return result.data

    def serialize(self, payload=None, many=False):
        """
        - DB'den gelen ObjectId değerlerini string'e dönüştürür.
        - UI'a gönderilirken kullanılır
        :param many:
        :param payload:
        :return:
        """

        if many:
            results = []
            for i in payload:
                item = self.serialize(i)
                results.append(item)
            return results

        result = self.dump(payload)
        return result.data

    def get_with_valid_json_payload(self, is_serializable=True):
        payload = request.json

        # Burası arıza çıkarabilir
        # self.serialize metodunun commentini address-add tarafında keyword eklemeden api'ya göndermek için kaldırdık
        if is_serializable is True:
            payload = self.serialize(payload)

        schema = self.deserialize(payload)
        return schema

    def get_with_valid_args_payload(self):
        payload = request.args

        schema = self.deserialize(payload)
        return schema

    def get_fields(self, *args):
        fields_list = self.fields
        keys = fields_list.keys()
        keys = set(keys)

        for exclude in args:
            keys.remove(exclude)

        return keys

    def unique_items_in_list(self, value):
        items = []

        for item in value:
            if item in items:
                raise Exception("Listede aynı kayıt zaten mevcut.", item)

            items.append(item)

        del items

    '''
    def to_obj(self):
        """
        Bu şemayı python objesine çevirir.
        :return: Python objesi geri döner.
        """
        obj = self.data
        return obj

    def to_schema(self, schema):
        """
        Bu şemayı parametrede verilen şemaya dönüştürür.
        :param schema: BaseSchema'dan kalıtılan bir şema olmalıdır.
        :return: Parametrede verilen şemanın doldurulmuş halini geri döner.
        """
        obj = self.to_obj()
        result = schema.load(obj)
        return result

    def from_obj(self, obj):
        """
        Bu şema, parametre ile verilen python objesi ile doldurulur.
        :param obj: Python objesi olmalıdır.
        :return: BaseSchema'dan kalıtılan bir şema geri döner.
        """
        schema = self.load(obj)
        return schema

    def from_schema(self, schema):
        """
        Bu şema, parametrede verilen şema ile doldurulur.
        :param schema: BaseSchema'dan kalıtılan bir şema olmalıdır.
        :return: Parametrede verilen şemanın doldurulmuş halini geri döner.
        """
        """
        obj = schema.data
        result = self.from_obj(obj)
        return result
        """
        result = self.dump(schema)
        return result

    '''

    """

    def to_obj(self, asd):
        obj = self.dump(asd)
        return obj

    def from_obj(self, obj):
        schema = self.load(obj)
        return schema

    def from_schema(self, schema):
        obj = schema.data
        result = self.from_obj(obj)
        return result

    def is_valid(self):
        obj = self.data

        try:
            validation_errors = self.validate(obj)

            if len(validation_errors.keys()) > 0:
                raise Exception(validation_errors)

            return True

        except ValidationError as err:
            raise ValidationError("request.validator.input_parameters_not_valid",
                                  "input parameters not valid : " + str(err))

        except Exception as err:
            raise ValidationError("request.validator.input_parameters_not_valid",
                                  "input parameters not valid : " + str(err))

    def get_with_valid_json_payload(self):
        payload = request.json
        schema = self.to_obj(payload)
        result = schema.is_valid()
        return result

    def get_with_valid_args_payload(self):
        payload = request.args

        schema = self.from_obj(payload)
        result = schema.is_valid()
        return result
    """

    """
    def from_schema(self, schema: Schema):
        if schema is None:
            raise ValidationError("request.validator.input_parameters_are_required", "input parameters not null")

        payload = schema.data
        result = self.from_load(payload)
        return result

    def from_load(self, payload):
        if payload is None:
            raise ValidationError("request.validator.input_parameters_are_required", "input parameters not null")

        result = self.load(payload)
        return result

    def validated(self):
        payload = self.data
        result = self.is_valid(payload)
        return result

    def is_valid(self, payload):
        if payload is None:
            raise ValidationError("request.validator.input_parameters_are_required", "input parameters not null")

        try:
            validation_errors = self.validate(payload)

            if len(validation_errors.keys()) > 0:
                raise Exception(validation_errors)

            obj = self.load(payload)
            # obj = schema.dump(payload)

            return obj.data

        except ValidationError as err:
            raise ValidationError("request.validator.input_parameters_not_valid",
                                  "input parameters not valid : " + str(err))

        except Exception as err:
            raise ValidationError("request.validator.input_parameters_not_valid",
                                  "input parameters not valid : " + str(err))

    def valid(self, payload):
        return self.is_valid(payload)

    def get_with_valid_payload(self, payload={}):
        return self.is_valid(payload)

    def get_with_valid_json_payload(self):
        payload = request.json
        return self.is_valid(payload)

    def get_with_valid_args_payload(self):
        payload = request.args
        data = self.is_valid(payload)
        return self.from_model(data)

    def from_model(self, model):
        result = self.dump(model)
        return result.data


    def unique_items_in_list(self, value):
        items = []

        for item in value:
            if item in items:
                raise Exception("Listede aynı kayıt zaten mevcut.", item)

            items.append(item)

        del items
        
    """
