import { get, post } from './https.js'

// 股票接口
export const stock_api = {

    /** 
     * 测试接口
     * 名称：exam
     * 参数：paramObj/null
     * 方式：fetch/post/patch/put
     */
    exam(paramObj) {
        return get('/stock/15', paramObj)
    },

    /**
     * 查询指数、行业、概念
     * @returns 
     */
    get_base(paramObj) {
        return get('/stock/base', paramObj)
    },

    /**
     * 根据指数、行业、概念找相关股票
     * @param {*} paramObj 
     * @returns 
     */
    get_base_stock(paramObj) {
        return get('/stock/base/stock', paramObj)
    },

    /** 
     * 指定股票（公司）接口
     * 名称：stock_company
     * 参数：paramObj/null
     * 方式：get
     */
    stock_company(code) {
        return get('/stock/' + code)
    },

    /** 
     * 模糊查询股票（公司）接口
     * 参数：paramObj/null
     * 方式：get
     */
    get_stocks(paramObj) {
        return get('/stock/stocks', paramObj)
    },

    /** 
     * 龙虎榜数据接口
     * 名称：stock_company
     * 参数：paramObj/null
     * 方式：get
     */
     get_stock_tiger() {
        return get('/stock/dt')
    },

    /** 
     * 今日提示数据接口
     * 名称：stock_company
     * 参数：paramObj/null
     * 方式：get
     */
     get_stock_note() {
        return get('/stock/note')
    },

    /** 
     * 周涨跌数据接口
     * 名称：stock_company
     * 参数：paramObj/null
     * 方式：get
     */
     get_stock_week_updown() {
        return get('/stock/week/updown')
    },

    /** 
     * 月涨跌数据接口
     * 名称：stock_company
     * 参数：paramObj/null
     * 方式：get
     */
     get_stock_month_updown() {
        return get('/stock/month/updown')
    },

    /** 
     * 股票实时数据接口
     * 名称：get_stock_day
     * 参数：paramObj/null
     * 方式：get
     */
    get_stock_day(code) {
        return get('/stock/real/' + code)
    },

    /** 
     * 买卖五档口数据接口
     * 名称：get_stock_trace
     * 参数：paramObj/null
     * 方式：get
     */
    get_stock_trace(code) {
        return get('/stock/trace/' + code)
    },


    /** 
     * 当天分时数据接口
     * 名称：get_stock_daytimedeal
     * 参数：paramObj/null
     * 方式：get
     */
    get_stock_daytimedeal(code) {
        return get('/stock/timedeal/' + code)
    },

    /** 
     * 当天分时实时数据接口
     * 名称：get_stock_realtimedeal
     * 参数：paramObj/null
     * 方式：get
     */
    get_stock_realtimedeal(code, level) {
        return get('/stock/timedeal/' + code + '/' + level)
    },

    /** 
     * 历史分时数据接口
     * 名称：get_stock_hist_realtimedeal
     * 参数：paramObj/null
     * 方式：get
     */
    get_stock_hist_realtimedeal(code, level,param) {
        return get('/stock/hist/timedeal/' + code + '/' + level,param)
    },




    //删除
       delete_stock(paramObj) {
        return get('/stock/delete-stock',paramObj)
    },


     update_company(paramObj) {
        return post('/stock/update-company', paramObj)
    },


    add_company(paramObj) {
        return post('/stock/add-company', paramObj)
    },




}

// 用户接口
export const user_api = {
    /** 
     * 登录
     * 名称 login
     * 参数：paramObj/null
     * 方式：fetch/post/patch/put
     */
    login(paramObj) {
        return post('/auth/login', paramObj)
    },

    /**
     *
     * 获取用户信息
     * 名称 user_info
     * 参数：paramObj/null
     * 方式：fetch/post/patch/put
     *
     * @returns 
     */
    user_info() {
        return get('/auth/user')
    },


//获取全部用户
    get_users(paramObj) {
        return get('/auth/users', paramObj)
    },


//按照名称搜索用户
      get_userbyname(paramObj) {
        return get('/auth/userbyname', paramObj)
    },
    /** 
     * 注册
     * 名称 register
     * 参数：paramObj/null
     * 方式：fetch/post/patch/put
     */
    register(paramObj) {
        return post('/auth/sign-in', paramObj)
    },
    /** 
     * 登出
     * 名称 logout
     * 参数：paramObj/null
     * 方式：fetch/post/patch/put
     */
    logout() {
        return get('/auth/logout')
    },



    delete_user(paramObj) {
        return get('/auth/delete-user',paramObj)
    },

    update(paramObj) {
        return post('/auth/update-user', paramObj)
    },

}



//支付接口
export const alipay_api={
 //    充值
 recharge(paramObj) {
        return get('/auth/recharge',paramObj)
    },

 addasset(paramObj) {
        return get('/auth/addasset',paramObj)
    },

 buystock(paramObj) {
        return get('/auth/buystock',paramObj)
    },

get_stock(paramObj){
     return get('/auth/get-stock',paramObj)
},
get_stocks(paramObj){
     return get('/auth/get-stocks',paramObj)
},


     del_stock(paramObj) {
        return get('/auth/del-stock', paramObj)
    },
     update_stock(paramObj) {
        return get('/auth/update-stock', paramObj)
    },
     q_one(paramObj) {
        return get('/auth/q-one', paramObj)
    },
     q_all() {
        return get('/auth/q-all')
    },

     sell(paramObj) {
        return get('/auth/sell',paramObj)
    },

    update_profit(paramObj) {
        return get('/auth/update-profit',paramObj)
    },


 tq(paramObj) {
        return get('/auth/tq',paramObj)
    },



}








