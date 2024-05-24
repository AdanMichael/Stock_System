# coding:utf-8
# 用户信息逻辑处理

from models.AccountModel import AccountModel  # 公司模型
from models.AccountStockModel import AccountStockModel
from models import db

class UserService(object):

    @classmethod
    def query_users(cls, limit: int , offset: int ):
        """
        分页查询用户
        :param limit:
        :param offset:
        :return:limit(limit).offset(offset).
        """
        result = {'accounts': [], 'sum': 0}
        accounts = AccountModel.query.filter(AccountModel.role == 'user' ).order_by(
            AccountModel.id).all()
        # 转化json格式
        if accounts is not None:
            for item in accounts:
                result['accounts'].append(item.to_json())
            result['sum'] = len(result.get('accounts'))
        return result



    @classmethod
    def query_user_byname(cls, name: str):
        result = {'accounts': [],'sum': 0}
        accounts = AccountModel.query.filter(AccountModel.nickname == name or AccountModel.phone==name or AccountModel.id==name).all()
        # 转化json格式
        if accounts is not None:
            for item in accounts:
                result['accounts'].append(item.to_json())
            result['sum'] = len(result.get('accounts'))
        return result


    # @classmethod
    # def delete_user_byid(cls, di: int):
    #
    #     account = AccountModel.query.filter(AccountModel.id == di).all()
    #     db.session.delete(account)
    #     db.session.commit()


    @classmethod
    def query_stock(cls, userid: int,search:str):
        result = {'stocks': [],'sum': 0}
        stocks = AccountStockModel.query.filter( AccountStockModel.stockname==search and AccountStockModel.account_id==userid).order_by(
            AccountStockModel.index).all()
        # 转化json格式
        if stocks is not None:
            for item in stocks:
                result['stocks'].append(item.to_json())
            result['sum'] = len(result.get('stocks'))
        return result

    @classmethod
    def query_stocks(cls, userid: int ):
        result = {'stocks': [], 'sum': 0}
        stocks = AccountStockModel.query.filter(AccountStockModel.account_id == userid).order_by(
            AccountStockModel.index).all()
        # 转化json格式
        if stocks is not None:
            for item in stocks:
                result['stocks'].append(item.to_json())
            result['sum'] = len(result.get('stocks'))
        return result

