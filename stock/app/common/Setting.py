# coding:utf-8
# 数据库配置文件

class Config(object):
    """ 基础配置文件 """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/stock_exchange'  # 数据库配置连接
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'stock_exchange'  # flaks 密钥


class DevelopmentConfig(Config):
    """ 开发环境 """
    ENV = 'development'
    DEBUG = True


class ProductionConfig(Config):
    """ 生产环境 """
    ENV = 'production'
    DEBUG = False

# 支付宝支付相关配置
import os
ALIPAY_SETTING = {
    'ALIPAY_APP_ID': 9021000137617824,  # 应用ID(上线之后需要改成，真实应用的appid)
    'APLIPAY_APP_NOTIFY_URL': None,  # 应用回调地址[支付成功以后,支付宝返回结果到哪一个地址下面] 一般这里不写，用下面的回调网址即可
    'ALIPAY_DEBUG': False,
    # APIPAY_GATEWAY="https://openapi.alipay.com/gateway.do"   # 真实网关
    'APIPAY_GATEWAY': "https://openapi.alipaydev.com/gateway.do",  # 沙盒环境的网关(上线需要进行修改)
    'ALIPAY_RETURN_URL': "http://127.0.0.1:8000/alipay/result/",  # 同步回调网址--用于前端,支付成功之后回调
    'ALIPAY_NOTIFY_URL': "http://127.0.0.1:8000/alipay/result/",  # 异步回调网址---后端使用，post请求，网站未上线，post无法接收到响应内容，付成功之后回调
    'APP_PRIVATE_KEY_STRING': os.path.join("../stock/app/alipay", 'app_private_key.pem'),  # 自己生成的私钥，这个就是路径拼接，配置好了，试试能不能点进去
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,********
    'ALIPAY_PUBLIC_KEY_STRING': os.path.join("../stock/app/alipay", 'alipay_public_key.pem'),  # 一定要注意，是支付宝给你的公钥，不是你自己生成的那个
    'SIGN_TYPE': "RSA2",  # RSA 或者 RSA2  现在基本上都是用RSA2

}

