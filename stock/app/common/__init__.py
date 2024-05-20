from alipay import AliPay
# 支付宝支付相关配置
ALIPAY_SETTING = {
    'ALIPAY_APP_ID': '9021000137617824',  # 应用ID(上线之后需要改成，真实应用的appid)
    'ALIPAY_DEBUG': False,
    'APIPAY_GATEWAY': 'https://openapi.alipaydev.com/gateway.do',  # 沙盒环境的网关(上线需要进行修改)
    'ALIPAY_RETURN_URL': None,  # 同步回调网址--用于前端,支付成功之后回调
    'ALIPAY_NOTIFY_URL': 'www.baidu.com',  # 异步回调网址---后端使用，post请求，网站未上线，post无法接收到响应内容，付成功之后回调
    'APP_PRIVATE_KEY_STRING': '../alipay/app_private_key.pem',  # 自己生成的私钥，这个就是路径拼接，配置好了，试试能不能点进去
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,********
    'ALIPAY_PUBLIC_KEY_STRING':'../alipay/alipay_public_key.pem',  # 一定要注意，是支付宝给你的公钥，不是你自己生成的那个
    'SIGN_TYPE': 'RSA2',  # RSA 或者 RSA2  现在基本上都是用RSA2
}
def alipay_obj():
    alipay = AliPay(
        appid=ALIPAY_SETTING.get('ALIPAY_APP_ID'),
        app_notify_url=None,  # 默认回调 url
        app_private_key_string=open(ALIPAY_SETTING.get('APP_PRIVATE_KEY_STRING')).read(),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=open(ALIPAY_SETTING.get('ALIPAY_PUBLIC_KEY_STRING')).read(),
        sign_type=ALIPAY_SETTING.get('SIGN_TYPE'),  # RSA 或者 RSA2
        debug=ALIPAY_SETTING.get('ALIPAY_DEBUG'),  # 默认 False
        verbose=False,  # 输出调试数据
        # config=AliPayConfig(timeout=50)  # 可选，请求超时时间
    )
    return alipay
if __name__ == '__main__':
    ap=alipay_obj()
    # 电脑网站支付，需要跳转到：https://openapi.alipay.com/gateway.do? + order_string
    url = ap.api_alipay_trade_page_pay(
    out_trade_no="20161112",
    total_amount=10,
    subject="测试订单",
    return_url=None,
    notify_url=None # 可选，不填则使用默认 notify url
    )
    pay_url = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do?' + url
    print(pay_url)


