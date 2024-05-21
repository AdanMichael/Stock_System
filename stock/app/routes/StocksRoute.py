# coding:utf-8
# 股票详细信息路由
import json
from datetime import timedelta
import pandas
import pandas as pd
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from flask import Blueprint, request
from common.Ig507Api import StockApi
from service.StockService import StockService
from common.Utils import resp, request_parse, pagination
from common.ResponseEnum import ResponseEnum

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')


@stock_bp.route('/init/stocks', methods=['PUT'])
def init_all_stocks():
    """
    初始化股票（公司）列表接口，数据量较大，需要花费2小时左右，不可轻易调用
    :return:
    """
    try:
        StockService.init_all_stocks()
        return resp()
    except Exception as e:
        print("股票（公司）列表接口异常 " + str(e))
        return resp(ResponseEnum.INIT_DATABASE_ERROR.value['code'], ResponseEnum.INIT_DATABASE_ERROR.value['msg'])


@stock_bp.route('/init/bases', methods=['PUT'])
def init_base_in_db():
    """
    初始化指数、行业、概念，不可轻易调用
    :return:
    """
    try:
        StockService.init_bases()
        return resp()
    except Exception as e:
        print("更新指数、行业、概念接口异常 " + str(e))
        return resp(ResponseEnum.INIT_DATABASE_ERROR.value['code'], ResponseEnum.INIT_DATABASE_ERROR.value['msg'])


# @stock_bp.route('/init/stock-base')
# def init_base_and_stock():
#     """
#     初始化指数、行业、概念与股票的关系表，不可轻易调用
#     :return:
#     """
#     try:
#         StockService.init_stock_and_base()
#         return resp()
#     except Exception as e:
#         print("初始化指数、行业、概念与股票的关系表接口异常：" + str(e))
#         return resp(ResponseEnum.INIT_DATABASE_ERROR.value['code'], ResponseEnum.INIT_DATABASE_ERROR.value['msg'])


@stock_bp.route('/base', methods=['GET'])
def get_base():
    """
    查询指数、行业、概念
    :param level
    :param pcode (可选)
    :return:
    """
    try:
        param = request_parse(request)
        data = StockService.query_base_by_level_and_pcode_and_type(param.get('level'), param.get('pcode'),
                                                                   param.get('type'))
        return resp(data=data)
    except Exception as e:
        print("查询指数、行业、概念接口异常 " + str(e))
        return resp(ResponseEnum.QUERY_DATABASE_FAIL.value['code'], ResponseEnum.QUERY_DATABASE_FAIL.value['msg'])


@stock_bp.route('/base/stock', methods=['GET'])
def get_stocks_by_base():
    """
    根据指数、行业、概念找相关股票
    :param tree_code
    :param pagelimit
    :param pagenum
    :return:
    """
    try:
        param = request_parse(request)
        limit, offset = 10, 1
        if param.get('pagelimit') is not None and param.get('pagenum') is not None:
            if param.get('tree_code') is not None:
                print(limit, offset)
                data = StockService.query_stock_by_base(param.get('tree_code'), int(param.get('pagelimit')),
                                                        int(param.get('pagenum')))
                return resp(data=data)
        return resp(ResponseEnum.PARAM_INVALID.value['code'],
                    ResponseEnum.PARAM_INVALID.value['msg'])
    except Exception as e:
        print("查询指数、行业、概念接口异常 " + str(e))
        return resp(ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['code'],
                    ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['msg'])


@stock_bp.route('/stocks', methods=['GET'])
def get_stocks():
    """
    股票详细信息分页查询接口（支持模糊查询和精确查询）
    :param stockname
    :param pagelimit
    :param pagenum
    :return:
    """
    try:
        param = request_parse(request)
        limit, offset = 10, 1
        if param.get('pagelimit') is not None and param.get('pagenum') is not None:
            limit, offset = pagination(param.get('pagelimit'), param.get('pagenum'))
        data = StockService.query_stock_by_like(stock_code=param.get('stockcode'),
                                                stock_name=param.get('stockname'),
                                                limit=limit,
                                                offset=offset)
        return resp(data=data)
    except Exception as e:
        print('股票公司名称查询接口异常 ' + str(e))
        return resp(ResponseEnum.QUERY_DATABASE_FAIL.value['code'], ResponseEnum.QUERY_DATABASE_FAIL.value['msg'])


@stock_bp.route('/<string:code>', methods=['GET'])
def get_stock_company(code):
    """
    单一股票公司列表接口
    :param code: 股票代码
    :return:
    """
    try:
        # 从数据库读取
        company = StockService.query_stock_company_by_code(code)
        if company is None:
            return resp(ResponseEnum.COMPANY_NOT_FOUND.value['code'], ResponseEnum.COMPANY_NOT_FOUND.value['msg'])
        return resp(data=company)
    except Exception as e:
        print('单一股票公司列表接口异常 ' + str(e))
        return resp(ResponseEnum.QUERY_DATABASE_FAIL.value['code'], ResponseEnum.QUERY_DATABASE_FAIL.value['msg'])


# ====================================
# 查询股市实时数据
# ====================================

@stock_bp.route('/real/<string:code>', methods=['GET'])
def get_stock_day(code):
    """
    股票实时数据接口
    :param code: 股票代码
    :return:
    """
    try:
        return resp(data=StockApi.get_stock_real(code))
    except Exception as e:
        print('股票实时数据接口异常 ' + str(e))
        return resp(ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['code'],
                    ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['msg'])


@stock_bp.route('/trace/<string:code>', methods=['GET'])
def get_stock_trace(code):
    """
    买卖五档口数据接口
    :param code: 股票代码
    :return:
    """
    try:
        return resp(data=StockApi.get_stock_trace5(code))
    except Exception as e:
        print('买卖五档口数据接口异常 ' + str(e))
        return resp(ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['code'],
                    ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['msg'])


@stock_bp.route('/timedeal/<string:code>', methods=['GET'])
def get_stock_daytimedeal(code):
    """
    当天分时数据接口
    :param code: 股票代码
    :return:
    """
    try:
        return resp(data=StockApi.get_stock_daytimedeal(code))
    except Exception as e:
        print('当天分时数据接口异常 ' + str(e))
        return resp(ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['code'],
                    ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['msg'])


@stock_bp.route('/timedeal/<string:code>/<string:level>', methods=['GET'])
def get_stock_realtimedeal(code, level):
    """
    当天分时实时数据接口
    :param code: 股票代码
    :param level: 分时级别
    :return:
    """
    try:

        if level in ['5', '15', '30', '60', 'Day', 'Week', 'Month', 'Year']:
            return resp(data=StockApi.get_stock_realtimedeal(code, level))
        else:
            return resp(ResponseEnum.STOCK_LEVEL_INVALID.value['code'],
                        ResponseEnum.STOCK_LEVEL_INVALID.value['msg'])

    except Exception as e:
        print('当天分时实时数据接口异常 ' + str(e))
        return resp(ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['code'],
                    ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['msg'])

############################################################机器学习！！！！！！！！！！！！！！！！
@stock_bp.route('/hist/timedeal/<string:code>/<string:level>', methods=['GET'])
def get_stock_hist_realtimedeal(code, level):
    # """
    # 历史分时数据接口
    # :param code: 股票代码
    # :param level: 分时级别
    # :return:
    # """
    #   pandas dropna:丢弃空值 ，numpy mean：取平均值 ， pandas resample:重采样
    # [a:b]表示切片  list[start_index:end_index:step]
    # start_index:表示起始索引
    # end_index:表示结束索引（不包含该索引对应的值）
    try:
        if level in ['5', '15', '30', '60', 'Day', 'Week', 'Month', 'Year']:
            return resp(data=StockApi.get_stock_hist_realtimedeal(code, level))
        elif level == 'Forecast':
            param=request_parse(request)
            cmd=param.get('cmd')
            data1 = pandas.DataFrame(StockApi.get_stock_hist_realtimedeal(code, 'Day'))
            #获取最后一个时间序列并去掉内部-，即2024-05-17 ——> 20240517 str类型
            # time=(data1['d'].iloc[-1]).replace('-', '')
            data1.to_csv('./data/Day.csv', index=False)
            #从2000到2024
            data = pd.read_csv('./data/Day.csv', index_col=0, parse_dates=[0],skiprows=range(1,2170))
            for_index = pd.read_csv('./data/Day.csv',  parse_dates=[0],skiprows=range(1,2170))
            # stock_week = data['c'].resample('W').mean().dropna()
            # stock_train = stock_week['2000':'2020'].dropna()
            # stock_data = stock_week['2021':'2022'].dropna()
            # print(stock_train)
            end = (for_index.tail(1).index.tolist())[0]
            # stock_data = data['c'].dropna()
            stock_data = data[cmd].dropna()
            #######
            new = data.index + timedelta(days=1)
            stock_train = data.set_index(new)
            ########
            # 确定模型参数d
            # stock_diff1 = stock_train.diff(1)[cmd].dropna()
            # 使用aic 准则法   确定p和q的值
            # res = sm.tsa.arma_order_select_ic(stock_diff1, max_ar=5, max_ma=5, ic=['aic'])
            # p=int(res.aic_min_order[0])
            # q=int(res.aic_min_order[1])
            # print(res.aic_min_order)
            # print(p)
            # print(q)
            model = ARIMA(stock_train [cmd].dropna(), order=(2, 1, 4))      #ARIMA算法模型
            # model = ARIMA(stock_train [cmd].dropna(), order=(p, 1, q))      #ARIMA算法模型
            re = model.fit()
            pred = re.predict(end-7,end, dynamic=True)      #预测
            # print(pred)
            ###################################################
            list1 = []
            list2 = []
            j=0
            for item in stock_data.index[end-7:end+1]:
                # print(str(item))
                tmp1 = {"date": str(item)[0:10], "val": format(stock_data[str(item)], '.2f')}
                j = j+1
                list1.append(tmp1)
            ########################################################
            i=0
            for item in stock_train.index[end-7:end+1]:
                # print(str(item))
                tmp2 = {"date": str(item)[0:10], "val": format(pred[i], '.2f')}
                i=i+1
                list2.append(tmp2)
     ##############################################
            json_origin = json.dumps(list1)
            json_pred = json.dumps(list2)
            print(list1)
            print(list2)
            obj = {'origin': json_origin, 'pred': json_pred}
            return resp(data=json.dumps(obj))
        else:
            return resp(ResponseEnum.STOCK_LEVEL_INVALID.value['code'],
                        ResponseEnum.STOCK_LEVEL_INVALID.value['msg'])
    except Exception as e:
        print('历史分时数据接口异常 ' + e)
        return resp(ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['code'],
                    ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['msg'])


@stock_bp.route('/week/updown', methods=['GET'])
def get_stock_week_updown():
    """
    周涨跌数据接口
    :return:
    """
    try:
        data = StockApi.get_updown_week()
        if data is not None:
            return resp(data=data)
        raise Exception
    except Exception as e:
        print('周涨跌数据接口异常 ' + str(e))
        return resp(ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['code'],
                    ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['msg'])


@stock_bp.route('/month/updown', methods=['GET'])
def get_stock_month_updown():
    """
    月涨跌数据接口
    :return:
    """
    try:
        data = StockApi.get_updown_month()
        if data is not None:
            return resp(data=data)
        raise Exception
    except Exception as e:
        print('周涨跌数据接口异常 ' + str(e))
        return resp(ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['code'],
                    ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['msg'])


@stock_bp.route('/dt', methods=['GET'])
def get_stock_dragon_tiger_list():
    """
    龙虎榜数据接口
    :return:
    """
    try:
        data = StockApi.get_dragon_tiger_list()
        if data is not None:
            return resp(data=data)
        raise Exception
    except Exception as e:
        print('龙虎榜数据接口异常 ' + str(e))
        return resp(ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['code'],
                    ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['msg'])


@stock_bp.route('/note', methods=['GET'])
def get_stock_note():
    """
    今日提醒数据接口
    :return:
    """
    try:
        data = StockApi.get_note()
        if data is not None:
            return resp(data=data)
        raise Exception
    except Exception as e:
        print('今日提醒数据接口异常 ' + str(e))
        return resp(ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['code'],
                    ResponseEnum.OUTER_INTERFACE_EXCEPTION.value['msg'])


@stock_bp.route('/delete-stock', methods=['GET'])
def delete_stock():
        param = request_parse(request)
        data=StockService.del_stock_company_by_code(param.get('code'))
        return resp(data=data)


@stock_bp.route('/update-company', methods=['POST','GET'])
def update():
        param = request_parse(request)
        res = StockService.update_stock_company_by_code(param)
        return resp(data=res)


@stock_bp.route('/add-company', methods=['POST','GET'])
def add():
        param = request_parse(request)
        res = StockService.add_stock_company_by_code(param)
        return resp(data=res)
