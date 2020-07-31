import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from eventlet.green import ssl
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

def email(_to, subject, body):
    _from = "admin@main.com"
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = _from
    message["To"] = _to

    # Turn these into plain/html MIMEText objects
    part = MIMEText(body, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    message.attach(part)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("mail.main.com", 465, context=context) as server:
        server.login(_from, "Japanitoes")
        if server.sendmail(_from, _to, message.as_string()):
            return True
        else:
            return False

