from flask import Flask, render_template
from flask_cors import CORS

import common.Setting as settings
import models
import routes


def create_app():
    # app = Flask(__name__, static_folder='dist/static', template_folder='dist')  # app核心对象(本地使用)
    app = Flask(__name__)  # app核心对象(本地使用)

    # 设置跨域请求
    CORS(app, supports_credentials=True)

    app.config.from_object(settings.ProductionConfig)  # 加载配置

    models.init_app(app)
    routes.init_app(app)

    # # 配置首页路由
    # @app.route('/', methods=['GET'])
    # def index():
    #     return render_template('index.html')
    #
    # # 只能从前端跳转页面
    # @app.route('/', defaults={'path': ''})
    # @app.route('/<path:path>')
    # def catch_all(path):
    #     return render_template("index.html")

    return app


if __name__ == '__main__':

    app = create_app()
    app.run(host='0.0.0.0', port=5000)