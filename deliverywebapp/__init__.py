import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ae98b899c219ea14930e01ecaafd451090f4276f6e3c20481d92d240acb35d47'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2020@localhost/delivery_webapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
migrate = Migrate(db)


from deliverywebapp.routes import routes, product_route, \
        area_routes, product_prices_route, bill_routes, \
        expense_categories_routes, raw_material_items_routes, \
        unit_of_measure_routes, supplier_routes, petty_cash_routes, \
        customer_routes, order_routes, account_info_route, example_route, \
        view_deliveries_routes, itemUom_routes, conversion_factors_routes, \
        update_material_quantities_routes, view_deliveries_routes, \
        view_quantity_balances_routes, update_daily_production_route, \
        view_daily_production_route, update_packaging_material_route, \
        view_packaging_material_balances_routes, reset_request_route, \
        reset_token_route

    #return app






