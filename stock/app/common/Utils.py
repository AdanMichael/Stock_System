# coding:utf-8
# 功能函数

import functools
from flask import request, jsonify, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from models.AccountModel import AccountModel  # 账户模型
from models import db
from common.ResponseEnum import ResponseEnum


def resp(code=ResponseEnum.SUCCESS.value['code'], msg=ResponseEnum.SUCCESS.value['msg'], data=None) -> object:
    """
    返回函数
    :param code 状态码
    :param msg 状态信息
    :param data 数据
    """
    try:
        result = {'code': code, 'msg': msg, 'data': data}
        return jsonify(result)
    except Exception as e:
        print(f'返回函数错误:{e}')


def request_parse(req_data):
    """
    解析请求数据并以json形式返回
    :param req_data:
    :return:
    """
    data = None
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data


def pagination(pagelimit, pagenum) -> tuple([int, int]):
    """
    分页查询
    :param pagelimit 每页数量
    :param pagenum 页码
    """
    try:
        pagelimit = int(pagelimit)
        pagenum = int(pagenum)
        offset = pagelimit * (pagenum - 1)
        return pagelimit, offset
    except Exception as e:
        print(f'分页函数错误: {e}')


#######################
# 用户身份验证
#######################


def valid_login(phone: str):
    """
    登陆验证
    :param phone 手机号
    """
    if len(phone) != 11:
        return False, ResponseEnum.SIGN_IN_PHONE_ERROR
    return True, ''


def valid_register(phone: str, password: str):
    """
    注册验证
    :param 手机号
    :param 密码
    """

    if len(phone) != 11:
        return False, ResponseEnum.SIGN_IN_PHONE_ERROR
    if len(password) < 5:
        return False, ResponseEnum.SIGN_IN_SECRET_ERROR
    return True, ''


def create_token(api_user):
    """
    生成token
    :param api_user 用户 id
    :return token
    """

    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=3600)
    # 接收用户id转换与编码
    token = s.dumps({"id": api_user}).decode("ascii")
    return token


def verify_token(token):
    """
    校验token
    :param token:
    :return: 用户信息 or None
    """

    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        # 转换为字典
        data = s.loads(token)
    except Exception:
        return None
    # 拿到转换后的数据，根据模型类去数据库查询用户信息
    account = db.session.query(AccountModel).filter(
        AccountModel.phone == data['id']).one()
    return account.to_json()


#######################
# 装饰器
#######################


def login_required(func):
    @functools.wraps(func)
    def verify_token(*args, **kwargs):
        try:
            # 在请求头上拿到token
            token = request.headers["token"]
        except Exception:
            # 没接收的到token,给前端抛出错误
            # 这里的code推荐写一个文件统一管理。这里为了看着直观就先写死了。
            return jsonify(code=ResponseEnum.EMPTY_TOKEN.value['code'], msg=ResponseEnum.EMPTY_TOKEN.value['msg'])

        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            s.loads(token)
        except Exception:
            return jsonify(code=ResponseEnum.LOGIN_EXPIRED.value['code'], msg=ResponseEnum.LOGIN_EXPIRED.value['msg'])

        return func(*args, **kwargs)

    return verify_token



from alipay import AliPay
# 支付宝支付相关配置
def alipay_obj():
    ALIPAY_SETTING = {
        'ALIPAY_APP_ID': '9021000137617824',  # 应用ID(上线之后需要改成，真实应用的appid)
        'ALIPAY_DEBUG': False,
        'APIPAY_GATEWAY': 'https://openapi.alipaydev.com/gateway.do',  # 沙盒环境的网关(上线需要进行修改)
        'ALIPAY_RETURN_URL': 'http://127.0.0.1:8080/#/',  # 同步回调网址--用于前端,支付成功之后回调
        'ALIPAY_NOTIFY_URL': 'http://127.0.0.1:8080/#/',  # 异步回调网址---后端使用，post请求，网站未上线，post无法接收到响应内容，付成功之后回调
        'APP_PRIVATE_KEY_STRING': '/home/lhx/pyProjects/code/stock/app/alipay/app_private_key.pem',  # 自己生成的私钥，这个就是路径拼接，配置好了，试试能不能点进去
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,********
        'ALIPAY_PUBLIC_KEY_STRING': '/home/lhx/pyProjects/code/stock/app/alipay/alipay_public_key.pem',  # 一定要注意，是支付宝给你的公钥，不是你自己生成的那个
        'SIGN_TYPE': 'RSA2',  # RSA 或者 RSA2  现在基本上都是用RSA2
    }
    alipay = AliPay(
        appid=ALIPAY_SETTING.get('ALIPAY_APP_ID'),
        app_notify_url=ALIPAY_SETTING.get('ALIPAY_NOTIFY_URL'),  # 默认回调 url
        app_private_key_string=open(ALIPAY_SETTING.get('APP_PRIVATE_KEY_STRING')).read(),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=open(ALIPAY_SETTING.get('ALIPAY_PUBLIC_KEY_STRING')).read(),
        sign_type=ALIPAY_SETTING.get('SIGN_TYPE'),  # RSA 或者 RSA2
        debug=ALIPAY_SETTING.get('ALIPAY_DEBUG'),  # 默认 False
        verbose=False,  # 输出调试数据
        # config=AliPayConfig(timeout=50)  # 可选，请求超时时间

    )
    return alipay








