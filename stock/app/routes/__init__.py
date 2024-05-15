from .AuthRoute import auth_bp
from .StocksRoute import stock_bp


def init_app(app):
    app.register_blueprint(stock_bp)
    app.register_blueprint(auth_bp)
