# coding:utf-8
# 获取IG507外部金融数据

import requests


class StockApi(object):
    """ IG507 请求密钥 """
    license = '9F83CEA9-6399-A249-E1BC-94B317827892'

    @classmethod
    def get_stock_list(cls) -> list:
        """
        基础股票列表
        :return:
        """
        stock_list = []
        try:
            url = f'http://ig507.com/data/base/gplist?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                for item in resp.json():
                    stock_list.append({
                        'code': item['dm'],
                        'name': item['mc'],
                        'jys': item['jys']
                    })
        except Exception as e:
            print(f'股票基础列表错误:{e}')
        finally:
            return stock_list

    @classmethod
    def get_company(cls, code: str, stockname: str, jys: str) -> object:
        """
        公司简介
        :param code: 股票代码
        :param stockname: 股票名称
        :param jys: 交易所
        :return:
        """
        company = {}
        try:
            url = f'http://ig507.com/data/time/f10/info/{code}?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                company = {
                    'code': code,
                    'stockname': stockname,
                    'jys': jys,
                    'name': None if data['name'] == '' else data['name'],
                    'ename': None if data['ename'] == '' else data['ename'],
                    'market': None if data['market'] == '' else data['market'],
                    'idea': None if data['idea'] == '' else data['idea'],
                    'ldate': None if data['ldate'] == '' else data['ldate'],
                    'sprice': None if data['sprice'] == '' else data['sprice'],
                    'principal': None if data['principal'] == '' else data['principal'],
                    'rdate': None if data['rdate'] == '' else data['rdate'],
                    'rprice': None if data['rprice'] == '' else data['rprice'],
                    'instype': None if data['instype'] == '' else data['instype'],
                    'organ': None if data['organ'] == '' else data['organ'],
                    'phone': None if data['phone'] == '' else data['phone'],
                    'site': None if data['site'] == '' else data['site'],
                    'post': None if data['post'] == '' else data['post'],
                    'addr': None if data['addr'] == '' else data['addr'],
                    'oaddr': None if data['oaddr'] == '' else data['oaddr'],
                    'desc': None if data['desc'] == '' else data['desc']
                }
        except Exception as e:
            print(f'公司简介错误:{e}')
        finally:
            return company

    @classmethod
    def get_stock_real(cls, code: str) -> object:
        """
        股票实时数据
        :param code: 股票代码
        :return:
        """
        stock = {}
        try:
            url = f'http://ig507.com/data/time/real/{code}?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                stock = {
                    'fm': data['fm'],
                    'hs': data['hs'],
                    'lb': data['lb'],
                    'high': data['h'],
                    'low': data['l'],
                    'pc': data['pc'],
                    'p': data['p'],
                    'sz': data['sz'],
                    'cje': data['cje'],
                    'ud': data['ud'],
                    'volume': data['v'],
                    'yc': data['yc'],
                    't': data['t']
                }
        except Exception as e:
            print(f'股票实时数据错误:{e}')
        finally:
            return stock

    @classmethod
    def get_stock_trace5(cls, code: str) -> object:
        """
        买卖五档口数据
        :param code: 股票代码
        :return:
        """
        trace5 = {}
        try:
            url = f'http://ig507.com/data/time/real/trace/level5/{code}?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                trace5 = resp.json()
        except Exception as e:
            print(f'买卖五档口数据错误:{e}')
        finally:
            return trace5

    @classmethod
    def get_stock_daytimedeal(cls, code: str) -> object:
        """
        当天分时成交数据
        :param code: 股票代码
        :return:
        """
        deal = {}
        try:
            url = f'http://ig507.com/data/time/real/trace/timedeal/{code}?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                deal = resp.json()
        except Exception as e:
            print(f'当天分时成交数据错误:{e}')
        finally:
            return deal

    @classmethod
    def get_stock_realtimedeal(cls, code: str, level: str) -> object:
        """
        当天分时及级别成交数据
        :param code: 股票代码
        :param level: 分时级别 5、15、30、60、Day、Day_qfq（日线前复权）、Day_hfq（日线后复权）、Week、Week_qfq（周线前复权）、Week_hfq（周线后复权）、Month、Month_qfq（月线前复权）、Month_hfq（月线后复权）、Year、Year_qfq（年线前复权）、Year_hfq（年线后复权）
        :return:
        """
        deal = {}
        try:
            url = f'http://ig507.com/data/time/real/time/{code}/{level}?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                deal = resp.json()
        except Exception as e:
            print(f'当天分时及级别成交数据错误:{e}')
        finally:
            return deal

    @classmethod
    def get_stock_hist_realtimedeal(cls, code: str, level: str) -> object:
        """
        历史分时及级别成交数据
        :param code: 股票代码
        :param level: 分时级别
        :return:
        """
        deal = {}
        try:
            url = f'http://ig507.com/data/time/history/trade/{code}/{level}?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                deal = resp.json()
        except Exception as e:
            print(f'历史分时及级别成交数据错误:{e}')
        finally:
            return deal

    @classmethod
    def get_updown_week(cls) -> list:
        """
        周涨跌数据
        :return:
        """
        week = None
        try:
            url = f'http://ig507.com/data/all/zzdpm?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                week = resp.json()
        except Exception as e:
            print(f'周涨跌数据错误:{e}')
        finally:
            return week

    @classmethod
    def get_updown_month(cls) -> list:
        """
        月涨跌数据
        :return:
        """
        month = None
        try:
            url = f'http://ig507.com/data/all/yzdpm?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                month = resp.json()
        except Exception as e:
            print(f'月涨跌数据错误:{e}')
        finally:
            return month

    # ============================
    # 指数、行业、概念
    # ============================

    @classmethod
    def get_all_bases(cls) -> list:
        """
        获取指数、行业、概念（包括基金，债券，美股，外汇，期货，黄金等的代码）
        :return:
        """
        bases = []
        try:
            url = f'https://ig507.com/data/base/it?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                bases = resp.json()
        except Exception as e:
            print(f'获取指数、行业、概念错误:{e}')
        finally:
            return bases

    @classmethod
    def get_stock_from_base(cls, tree_code: str) -> list:
        """
        根据指数、行业、概念找相关股票
        :param tree_code: 指数、行业、概念代码
        :return:
        """
        stocks = []
        try:
            url = f'https://ig507.com/data/time/indextree/{tree_code}?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                stocks = resp.json()
        except Exception as e:
            print(f'根据指数、行业、概念找相关股票错误:{e}')
        finally:
            return stocks

    @classmethod
    def get_base_from_stock(cls, code: str) -> list:
        """
        根据股票找相关指数、行业、概念
        :param code: 股票代码
        :return:
        """
        bases = []
        try:
            url = f'https://ig507.com/data/time/iii/{code}?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                bases = resp.json()
        except Exception as e:
            print(f'根据股票找相关指数、行业、概念错误:{e}')
        finally:
            return bases

    # ============================
    # 沪深数据中心
    # ============================
    @classmethod
    def get_note(cls) -> object:
        """
        今日交易提示
        :return:
        """
        stocks = None
        try:
            url = f'https://ig507.com/data/all/tt?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                stocks = resp.json()
        except Exception as e:
            print(f'今日交易提示错误:{e}')
        finally:
            return stocks

    @classmethod
    def get_dragon_tiger_list(cls) -> list:
        """
        今日龙虎榜概览
        :return:
        """
        stocks = None
        try:
            url = f'https://ig507.com/data/all/ld?licence={cls.license}'
            resp = requests.get(url)
            if resp.status_code == 200:
                stocks = resp.json()
        except Exception as e:
            print(f'今日龙虎榜概览错误:{e}')
        finally:
            return stocks


if __name__ == '__main__':
    # 测试
    api = StockApi()
    # print(api.get_stock_list())
    # print(api.get_company('301235', '华康医疗', 'sz'))
    print(api.get_stock_real('605567'))
    # print(api.get_stock_trace5('000001'))
    # print(api.get_stock_daytimedeal('000001'))
    # print(api.get_stock_realtimedeal('000001', '5'))
    # print(api.get_stock_hist_realtimedeal('000001', '5'))
    # print(api.get_updown_week())
    # print(api.get_updown_month())
    # print(api.get_all_bases())
    # print(api.get_base_from_stock('000001'))
    # print(api.get_stock_from_base('sw_smls'))
    # print(api.get_note())
    # print(api.get_dragon_tiger_list())