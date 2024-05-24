# coding:utf-8
# 认证（登录/注册）路由
import decimal

from flask import Blueprint, request, session
from models.AccountModel import AccountModel  # 账户模型
from models.AccountStockModel import AccountStockModel  #购入股票模型
from service.UserService import UserService
from models import db
from common.Utils import create_token, login_required, resp, \
    valid_login, valid_register, verify_token, pagination, request_parse, ResponseEnum,alipay_obj
import time
from alipay import AliPay


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    登录
    :param phone
    :param password
    :return:
    """
    try:
        param = request_parse(request)
        account = valid_login(param.get('phone'))
        if account[0]:  # 电话格式合法
            account = db.session.query(AccountModel).filter(
                AccountModel.phone == param.get('phone'),
                AccountModel.password == param.get('password')).first()
            if account is not None:
                # 用户存在，创建token
                token = create_token(account.phone)
                session['token'] = token
                return resp(data={'token': token})
            else:

                return resp(ResponseEnum.USER_NOT_FOUND.value['code'], ResponseEnum.USER_NOT_FOUND.value['msg'])
        else:
            return resp(account[1].value['code'], account[1].value['msg'])
    except Exception as e:
        print('登录异常 ' + str(e))
        return resp(ResponseEnum.SYSTEM_ERROR.value['code'], ResponseEnum.SYSTEM_ERROR.value['msg'])


@auth_bp.route('/sign-in', methods=['POST'])
def sign_in():
    """
    注册
    :param phone
    :param password
    :param nickname
    :return:
    """
    try:
        param = request_parse(request)
        register = valid_register(param.get('phone'), param.get('password'))
        if register[0]:  # 数据是否合法
            account = repeat_register(param.get('phone'))
            if account[0]:  # 账户不存在
                last_id=(AccountModel.query.filter()[-1]).id+1  ##########新加
                account = AccountModel(
                                      id=last_id,  ########## 新加
                                       nickname=param.get('nickname'),
                                       phone=param.get('phone'),
                                       password=param.get('password'),
                                       role='user',
                                       create_time=round(time.time() * 1000))
                db.session.add(account)
                db.session.commit()
                # session.clear()
                return resp(data=account.to_json())
            else:
                return resp(ResponseEnum.USER_ALREADY_EXIST.value['code'], ResponseEnum.USER_ALREADY_EXIST.value['msg'])
        else:
            return resp(register[1].value['code'], register[1].value['msg'])
    except Exception as e:
        print('注册异常 ' + str(e))
        return resp(ResponseEnum.SYSTEM_ERROR.value['code'], ResponseEnum.SYSTEM_ERROR.value['msg'])


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    登出
    :return:
    """
    try:
        session.pop('token', None)
        return resp()
    except Exception as e:
        print('登出异常 ' + str(e))
        return resp(ResponseEnum.SYSTEM_ERROR.value['code'], ResponseEnum.SYSTEM_ERROR.value['msg'])


@auth_bp.route('/user', methods=['GET'])
@login_required
def get_userinfo():
    """
    用户信息
    :return:
    """
    token = request.headers["token"]
    # 拿到token，去换取用户信息
    return resp(data=verify_token(token))




@auth_bp.route('/users', methods=['GET'])
def get_users():
    """
    分页查询用户列表
    :param pagelimit
    :param pagenum
    :return:
    """
    try:
        param = request_parse(request)
        if param.get('pagelimit') is not None and param.get('pagenum') is not None:
            limit, offset = pagination(param.get('pagelimit'), param.get('pagenum'))
            data = UserService.query_users(limit, offset)
            return resp(data=data)


        else:
            return resp(ResponseEnum.PARAM_INVALID.value['code'], ResponseEnum.PARAM_INVALID.value['msg'])
    except Exception as e:
        print('分页查询用户列表异常 ' + str(e))
        return resp(ResponseEnum.QUERY_DATABASE_FAIL.value['code'], ResponseEnum.QUERY_DATABASE_FAIL.value['msg'])



@auth_bp.route('/userbyname', methods=['POST','GET'])
def get_userbyname():
        param = request_parse(request)
        name= param.get('nickname')
        data = UserService.query_user_byname(name)
        return resp(data=data)




@auth_bp.route('/delete-user', methods=['POST','GET'])
def delete_user():
        param = request_parse(request)
        res =db.session.query(AccountModel).filter(AccountModel.id == param.get('id')).delete()
        # db.session.delete(account)
        db.session.commit()
        return resp(res)


@auth_bp.route('/update-user', methods=['POST','GET'])
def update_user():
        param = request_parse(request)
        id=param.get('id')
        nname = param.get('nickname')
        phe = param.get('phone')
        pwd = param.get('password')
        rest_asset = param.get('rest_asset')
        profit_asset = param.get('profit_asset')
        if(rest_asset is None):
            rest_asset=0
        else:
            rest_asset=decimal.Decimal(rest_asset)
        if (profit_asset is None):
            profit_asset=0
        else:
            profit_asset = decimal.Decimal(profit_asset)

        user = valid_register(param.get('phone'), param.get('password'))
        if user[0]:  # 数据是否合法
                res = db.session.query(AccountModel).filter(AccountModel.id ==id ).update(
                    {'nickname':nname, 'phone':phe, 'password':pwd ,'rest_asset':rest_asset,'profit_asset':profit_asset}
                )
                db.session.commit()
                return resp(res)
        else:
            return resp(user[1].value['code'], user[1].value['msg'])


@auth_bp.route('/recharge', methods=['GET','POST'])
def recharge():
    param = request_parse(request)
    money=param.get('money')
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    ap=alipay_obj()
    url = ap.api_alipay_trade_page_pay(
        out_trade_no=now_time,
        total_amount=money,
        subject="充值订单",
        return_url='http://127.0.0.1:8080/#/profile',
        notify_url='http://127.0.0.1:8080/#/profile'
    )
    res = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do?' + url
    return resp(data=res)


@auth_bp.route('/addasset', methods=['GET','POST'])
def addasset():
    param = request_parse(request)
    money=decimal.Decimal(param.get('money'))
    id=param.get('id')
    user= db.session.query(AccountModel).filter(AccountModel.id == id).first()
    user.rest_asset+=money
    res=db.session.commit()
    return resp(res)

@auth_bp.route('/buystock', methods=['GET','POST'])
def buystock():
    param = request_parse(request)
    buy_price=decimal.Decimal(param.get('buy_price'))
    account_id=param.get('account_id')
    code_id=param.get('code_id')
    stocknum=decimal.Decimal(param.get('stocknum'))
    stockname=param.get('stockname')
    buy_time=param.get('buy_time')
    user = db.session.query(AccountModel).filter(AccountModel.id == account_id).first()
    if user.rest_asset>=(stocknum*buy_price):
        new=AccountStockModel(stockname=stockname,buy_price=buy_price,account_id=account_id,code_id=code_id,stocknum=stocknum,buy_time=buy_time)
        res=db.session.add(new)
        user.rest_asset -= stocknum*buy_price
        db.session.commit()
        return resp()
    else:
        return resp(ResponseEnum.NoMoney_ERROR.value['code'], ResponseEnum.NoMoney_ERROR.value['msg'])




@auth_bp.route('/get-stock', methods=['GET','POST'])
def get_stock():
    try:
        param = request_parse(request)
        userid=param.get('account_id')
        search=param.get('search')
        data = UserService.query_stock(userid,search)
        return resp(data=data)
    except Exception as e:
        print('分页查询用户列表异常 ' + str(e))
        return resp(ResponseEnum.QUERY_DATABASE_FAIL.value['code'], ResponseEnum.QUERY_DATABASE_FAIL.value['msg'])



@auth_bp.route('/get-stocks', methods=['GET','POST'])
def get_stocks():
    try:
        param = request_parse(request)
        userid = param.get('account_id')
        data = UserService.query_stocks(userid)
        return resp(data=data)
    except Exception as e:
        print('分页查询用户列表异常 ' + str(e))
        return resp(ResponseEnum.QUERY_DATABASE_FAIL.value['code'], ResponseEnum.QUERY_DATABASE_FAIL.value['msg'])




@auth_bp.route('/q-all', methods=['POST','GET'])
def q_all():
    try:
        data = UserService.q_all()
        return resp(data=data)
    except Exception as e:
        print('分页查询用户列表异常 ' + str(e))
        return resp(ResponseEnum.QUERY_DATABASE_FAIL.value['code'], ResponseEnum.QUERY_DATABASE_FAIL.value['msg'])



@auth_bp.route('/q-one', methods=['GET','POST'])
def q_one():
    try:
        param = request_parse(request)
        search = param.get('search')
        data = UserService.q_one(search)
        return resp(data=data)
    except Exception as e:
        print('分页查询用户列表异常 ' + str(e))
        return resp(ResponseEnum.QUERY_DATABASE_FAIL.value['code'], ResponseEnum.QUERY_DATABASE_FAIL.value['msg'])


@auth_bp.route('/del-stock', methods=['GET','POST'])
def del_stock():
        param = request_parse(request)
        index = param.get('index')
        res = db.session.query(AccountStockModel).filter(AccountStockModel.index == index).delete()
        db.session.commit()
        return resp(res)


@auth_bp.route('/update-stock', methods=['GET','POST'])
def update_stock():
        param = request_parse(request)
        index = param.get('index')
        stocknum = param.get('stocknum')
        buy_price = param.get('buy_price')
        profit = param.get('profit')
        res = db.session.query(AccountStockModel).filter(AccountStockModel.index == index).update(
            {'stocknum': stocknum, 'buy_price': buy_price, 'profit': profit}
        )
        db.session.commit()
        return resp(res)




############################################
# 辅助函数
############################################


def repeat_register(phone: str):
    """ 判断用户是否已经存在，存在False，不存在True """
    account = db.session.query(AccountModel).filter(
        AccountModel.phone == phone).first()
    if account is None:
        return True, ''
    else:
        return False, ''

