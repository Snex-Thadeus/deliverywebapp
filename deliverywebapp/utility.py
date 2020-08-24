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


def get_clean_price_value(price_value):
    return price_value.replace("Ksh ", '').replace(",", '').strip()


def get_id_for_choose_category(product_price_category, select):
    return_id = 1
    for i in range(len(product_price_category)):
        return_id = i
        if product_price_category[i] == select:
            break

    return return_id
    pass


def get_id_for_choose_method(product_price_method, select):
    return_id = 1
    for i in range(len(product_price_method)):
        return_id = i
        if product_price_method[i] == select:
            break

    return return_id


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
