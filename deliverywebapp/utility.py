from flask import json
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


def getCleanPriceValue(PRICE_VALUE):
    return PRICE_VALUE.replace("Ksh ", '').replace(",", '').strip()


def getIDForChooseCategory(PRODUCT_PRICE_CATEGORY, select):
    returnID = 1
    for i in range(len(PRODUCT_PRICE_CATEGORY)):
        returnID = i
        if PRODUCT_PRICE_CATEGORY[i] == select:
            break

    return returnID
    pass


def getIDForChooseMethod(PRODUCT_PRICE_METHOD, select):
    returnID = 1
    for i in range(len(PRODUCT_PRICE_METHOD)):
        returnID = i
        if PRODUCT_PRICE_METHOD[i] == select:
            break

    return returnID
