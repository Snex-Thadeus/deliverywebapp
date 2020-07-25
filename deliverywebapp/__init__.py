from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.debug = True

app.config["SECRET_KEY"] = 'ae98b899c219ea14930e01ecaafd451090f4276f6e3c20481d92d240acb35d47'
# basedir  = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:@localhost:3306/delivery_webapp_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

try:
    db = SQLAlchemy(app)
except sqlalchemy.exc.ProgrammingError as e:
    print("error", e)

ma = Marshmallow(app)

# init bcrypt
bcrypt = Bcrypt(app)

# init the login manager
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# setting the config options for mail
app.config["MAIL_USERNAME"] = "denniskiruku@gmail.com"
app.config["MAIL_PASSWORD"] = "*****"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_PORT"] = 587

mail = Mail()

migrate = Migrate(app, db)

from deliverywebapp.routes import routes, product_route, \
    area_routes, product_prices_route, bill_routes, \
    expense_categories_routes, raw_material_items_routes, \
    unit_of_measure_routes, supplier_routes, petty_cash_routes, \
    customer_routes, order_routes, account_info_route, example_route
