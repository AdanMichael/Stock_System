from enum import Enum


class ResponseEnum(Enum):
    SUCCESS = {'code': 200, 'msg': '成功'}
    EMPTY_TOKEN = {'code': 1001, 'msg': '缺少token参数'}
    LOGIN_EXPIRED = {'code': 1002, 'msg': '登录超时'}
    DATABASE_EXCEPTION = {'code': 1003, 'msg': '数据库异常'}
    UPDATE_DATABASE_FAIL = {'code': 1004, 'msg': '更新数据失败'}
    INSERT_DATABASE_FAIL = {'code': 1005, 'msg': '插入数据失败'}
    QUERY_DATABASE_FAIL = {'code': 1006, 'msg': '查询数据失败'}
    DELETE_DATABASE_FAIL = {'code': 1007, 'msg': '删除数据失败'}
    PARAM_INVALID = {'code': 1008, 'msg': '参数异常'}
    OUTER_INTERFACE_EXCEPTION = {'code': 1009, 'msg': 'IG507外部接口异常'}
    STOCK_LEVEL_INVALID = {'code': 1010, 'msg': '股票分时级别无效'}
    COMPANY_NOT_FOUND = {'code': 1011, 'msg': '公司信息不存在'}
    USER_NOT_FOUND = {'code': 1012, 'msg': '手机号或者密码错误'}
    LOGIN_INFO_INVALID = {'code': 1013, 'msg': '登录信息不合法'}
    SIGN_IN_FAIL = {'code': 1014, 'msg': '用户注册失败'}
    USER_ALREADY_EXIST = {'code': 1015, 'msg': '用户已经存在'}
    SIGN_IN_PHONE_ERROR = {'code': 1016, 'msg': '手机号码格式错误'}
    SIGN_IN_SECRET_ERROR = {'code': 1017, 'msg': '密码不能小于5位'}
    SYSTEM_ERROR = {'code': 1018, 'msg': '系统未知错误'}
    INIT_DATABASE_ERROR = {'code': 1019, 'msg': '初始化数据库失败'}


