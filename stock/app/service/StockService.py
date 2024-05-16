# coding:utf-8
# 股票信息查询逻辑处理

from common.Ig507Api import StockApi  # 开放接口
from models.StocksModel import StockModel  # 公司模型
from models.BaseModel import BaseModel
from models import db
import time


class StockService(object):

    @classmethod
    def init_all_stocks(cls):
        """
        获取市面股票最新数据，并更新数据库。数据量较大，需要花费2小时左右
        :return:
        """

        stock_list = StockApi.get_stock_list()
        for stock in stock_list:
            time.sleep(2)  # 限制请求频率
            stock_company = StockApi.get_company(stock['code'], stock['name'], stock['jys'])  # 获取公司详细信息
            sc = StockModel(code=stock_company['code'],
                            stockname=stock_company['stockname'],
                            jys=stock_company['jys'],
                            name=stock_company['name'],
                            ename=stock_company['ename'],
                            market=stock_company['market'],
                            idea=stock_company['idea'],
                            ldate=stock_company['ldate'],
                            sprice=stock_company['sprice'],
                            principal=stock_company['principal'],
                            rdate=stock_company['rdate'],
                            rprice=stock_company['rprice'],
                            instype=stock_company['instype'],
                            organ=stock_company['organ'],
                            phone=stock_company['phone'],
                            site=stock_company['site'],
                            post=stock_company['post'],
                            addr=stock_company['addr'],
                            oaddr=stock_company['oaddr'],
                            desc=stock_company['desc'])
            db.session.add(sc)
            db.session.commit()
            print(f"插入成功{sc.code}, {sc.stockname}, {sc.jys}")
        # 存储到数据库

    @classmethod
    def init_bases(cls):
        """
        更新数据库中的指数、行业、概念
        :return:
        """
        bases = StockApi.get_all_bases()
        for base in bases:
            sc = BaseModel(
                code=base['code'],
                name=base['name'],
                type1=base['type1'],
                type2=base['type2'],
                level=base['level'],
                pcode=base['pcode'],
                pname=base['pname'],
                isleaf=base['isleaf'],
            )
            db.session.add(sc)
            db.session.commit()
            print(f"更新成功 - {sc.code}, {sc.name}")
        # 存储到数据库

    @classmethod
    def init_stock_and_base(cls):
        bases = StockApi.get_all_bases()
        for base in bases[:2]:
            result = cls.query_base_by_level_and_pcode_and_type(base['level'], base['pcode'], base['type2'])
            print(result)

    @classmethod
    def query_base_by_level_and_pcode_and_type(cls, level_code: str = 0, pcode: str = None, types: str = None):
        """
        查询指数、行业、概念
        :param types: 类型
        :param pcode: 父节点
        :param level_code: 节点级别
        :return:
        """
        result = []
        if types is None:
            # 默认A股-分类板块
            types = 3
        filter_list = [BaseModel.level == level_code, BaseModel.type2 == types]
        if pcode is not None:
            filter_list.append(BaseModel.pcode == pcode)
        stock_bases = BaseModel.query.filter(*filter_list).order_by(BaseModel.level).all()
        # 转化json格式
        for item in stock_bases:
            result.append(item.to_json())
        return result

    @classmethod
    def query_stock_by_base(cls, tree_code: str = None, limit: int = 10, offset: int = 1):
        """
        根据指数、行业、概念分页查询股票
        :param tree_code:
        :param limit:
        :param offset:
        :return:
        """
        result = {'stocks': [], 'sum': 0}
        stocks = StockApi.get_stock_from_base(tree_code)
        t_stocks = []
        while len(stocks) != 0:
            t_stocks.append(stocks.pop(-1))
        if len(t_stocks) - offset <= limit:
            page_stocks = t_stocks[offset:]
        else:
            page_stocks = t_stocks[(offset - 1) * limit: offset * limit]
        result['stocks'] = page_stocks
        result['sum'] = len(t_stocks)
        return result

    @classmethod
    def query_stock_by_like(cls, stock_code: str = None, stock_name: str = None, limit: int = 10, offset: int = 1):
        """
        股票多条件模糊查询
        :param stock_code:
        :param stock_name:
        :param limit:
        :param offset:
        :return:
        """
        # 从数据库读取
        result = {'companies': [], 'sum': 0}
        companies = []
        companies_1 = StockModel.query.filter(StockModel.stockname.like("%" + stock_name + "%")).order_by(StockModel.code.asc()).limit(limit).offset(offset).all()
        companies_2 = StockModel.query.filter(StockModel.code.like("%" + stock_code + "%")).order_by(StockModel.code.asc()).limit(limit).offset(offset).all()
        companies.extend(companies_1)
        companies.extend(companies_2)
        _sum = StockModel.query.filter(StockModel.stockname.like("%" + stock_name + "%")).count()
        _sum = _sum + StockModel.query.filter(StockModel.code.like("%" + stock_code + "%")).count()
        # 转化json格式
        for item in companies:
            result['companies'].append(item.to_json())
        result['sum'] = _sum
        return result

    @classmethod
    def query_stock_company_by_code(cls, code: str):
        company = StockModel.query.filter(StockModel.code == code).first()
        if company is not None:
            return company.to_json()
        else:
            StockApi.get_company(code)


    @classmethod
    def del_stock_company_by_code(cls, code: str):
        res=StockModel.query.filter(StockModel.code == code).delete()
        db.session.commit()
        return res

    @classmethod
    def update_stock_company_by_code(cls, param: []):
        res=StockModel.query.filter(StockModel.code == param.get("code")).update({'stockname':param.get('stockname'),'jys':param.get('jys'),'name':param.get('name'),
        'ename':param.get('ename'),'market':param.get('market') ,'idea':param.get('idea'),'ldate':param.get('ldate'),
        'sprice':param.get('spricr'),'principal':param.get('principal') ,'rdate':param.get('rdate'),'rprice':param.get('rprice') ,
        'instype':param.get('instype'),'organ':param.get('organ'),'phone':param.get('phone'),'site':param.get('site'),
          'post':param.get('post') ,'addr':param.get('addr'), 'oaddr':param.get('oaddr'),'desc':param.get('desc')                                                                            })
        db.session.commit()
        return res



    @classmethod
    def add_stock_company_by_code(cls, param: []):
        last_one=StockModel.query.filter()[-1]
        lcode=str(int(last_one.code)+1)
        company=StockModel(
        code=lcode,
        stockname=param.get('stockname'),jys=param.get('jys'),name=param.get('name'),
        ename=param.get('ename'),market=param.get('market') ,idea=param.get('idea'),ldate=param.get('ldate'),
        sprice=param.get('spricr'),principal=param.get('principal') ,rdate=param.get('rdate'),rprice=param.get('rprice') ,
        instype=param.get('instype'),organ=param.get('organ'),phone=param.get('phone'),site=param.get('site'),
          post=param.get('post') ,addr=param.get('addr'), oaddr=param.get('oaddr'),desc=param.get('desc')
        )
        res=db.session.add(company)
        db.session.commit()
        return res

